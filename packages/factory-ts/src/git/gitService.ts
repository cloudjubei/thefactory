import fs from 'node:fs';
import path from 'node:path';
import { FileChangeManager, type FileChangeProposal, type ProposalId } from '../files/fileChangeManager';
import type { HistoryStore } from '../db/sqlite';

// We load simple-git lazily to keep the library light where git isn't needed.
// Consumers must add `simple-git` as a dependency when using this module.
let simpleGitFactory: any | null = null;
async function getSimpleGit(root: string) {
  if (!simpleGitFactory) {
    try {
      const mod = await import('simple-git');
      simpleGitFactory = (mod as any).simpleGit ?? (mod as any).default;
      if (!simpleGitFactory) throw new Error('simple-git not available');
    } catch (err) {
      throw new Error('simple-git is required for GitService. Please install it: npm i simple-git');
    }
  }
  return simpleGitFactory({ baseDir: root });
}

export type GitRepoInfo = {
  root: string;
  isRepo: boolean;
  currentBranch: string | null;
  headSha: string | null;
  isDetached: boolean;
  isClean: boolean;
};

export type CommitMetadata = Record<string, any> | undefined;

function normalizeAbs(p: string): string {
  return path.resolve(p);
}

function ensureInsideRoot(root: string, relOrAbs: string): string {
  const full = path.resolve(root, relOrAbs);
  const normalizedRoot = normalizeAbs(root);
  const rel = path.relative(normalizedRoot, full);
  if (rel.startsWith('..') || path.isAbsolute(rel)) {
    throw new Error(`Path escapes project root: ${relOrAbs}`);
  }
  return full;
}

function toGitPath(p: string): string {
  return p.split(path.sep).join('/');
}

function ensureDirForFile(filePath: string) {
  const dir = path.dirname(filePath);
  fs.mkdirSync(dir, { recursive: true });
}

export class GitService {
  private projectRoot: string;
  private store?: HistoryStore;
  private runId?: string;
  private git: any | null = null;
  private branchName: string | null = null;
  private appliedPaths = new Map<ProposalId, Set<string>>();
  private lastStashMessage: string | null = null;

  constructor(opts: { projectRoot: string; store?: HistoryStore; runId?: string }) {
    this.projectRoot = normalizeAbs(opts.projectRoot);
    this.store = opts.store;
    this.runId = opts.runId;
  }

  async ensureRepo(): Promise<GitRepoInfo> {
    const git = (this.git ??= await getSimpleGit(this.projectRoot));
    const isRepo = await git.checkIsRepo();
    if (!isRepo) {
      throw new Error(`Not a git repository: ${this.projectRoot}`);
    }
    const status = await git.status();
    const branches = await git.branch();
    let headSha: string | null = null;
    try {
      headSha = (await git.revparse(['HEAD']))?.trim() || null;
    } catch {
      headSha = null;
    }
    const info: GitRepoInfo = {
      root: this.projectRoot,
      isRepo: true,
      currentBranch: branches.current || null,
      headSha,
      isDetached: !!(branches as any).detached,
      isClean: status.isClean(),
    };
    return info;
  }

  async createFeatureBranch(runId?: string, nameFactory?: (runId: string) => string): Promise<{ branch: string; base: string | null; stashed: boolean }>
  {
    const info = await this.ensureRepo();
    const git = this.git!;
    const effectiveRunId = runId ?? this.runId;
    if (!effectiveRunId) throw new Error('createFeatureBranch requires a runId');

    const status = await git.status();
    let stashed = false;
    if (!status.isClean()) {
      const msg = `overseer-factory: stash for run ${effectiveRunId}`;
      await git.stash(['push', '-u', '-m', msg]);
      this.lastStashMessage = msg;
      stashed = true;
    }

    const base = info.headSha;
    const branch = (nameFactory ?? ((rid: string) => `overseer/run/${rid}`))(effectiveRunId);

    // Create/update branch from current HEAD (handle detached as well)
    if (info.isDetached) {
      // Create branch at specific commit
      await git.checkout(['-B', branch, base ?? 'HEAD']);
    } else {
      // Create local branch from current branch HEAD
      const allBranches = await git.branch();
      if (allBranches.all.includes(branch)) {
        await git.checkout(branch);
      } else {
        await git.checkoutLocalBranch(branch);
      }
    }

    this.branchName = branch;

    return { branch, base: base ?? null, stashed };
  }

  private assertOnFeatureBranch() {
    if (!this.branchName) throw new Error('No active feature branch; call createFeatureBranch first');
  }

  async applyProposalToBranch(proposalId: ProposalId, manager: FileChangeManager): Promise<{ appliedPaths: string[] }>
  {
    this.assertOnFeatureBranch();
    const git = this.git ?? (this.git = await getSimpleGit(this.projectRoot));
    const proposal = manager.getProposal(proposalId);
    if (!proposal) throw new Error(`Proposal not found: ${proposalId}`);
    if (proposal.status !== 'open') throw new Error(`Cannot apply proposal with status ${proposal.status}`);

    const branchInfo = await git.branch();
    const current = branchInfo.current || null;
    if (current !== this.branchName) {
      throw new Error(`Not on feature branch ${this.branchName}; current is ${current}`);
    }

    const changed = new Set<string>();

    for (const ch of proposal.changes) {
      if (ch.action === 'write') {
        const full = ensureInsideRoot(this.projectRoot, ch.path);
        ensureDirForFile(full);
        fs.writeFileSync(full, ch.content, 'utf8');
        const rel = toGitPath(path.relative(this.projectRoot, full));
        await git.add([rel]);
        changed.add(rel);
      } else if (ch.action === 'delete') {
        const full = ensureInsideRoot(this.projectRoot, ch.path);
        if (fs.existsSync(full)) fs.rmSync(full);
        const rel = toGitPath(path.relative(this.projectRoot, full));
        // Stage deletion; git.rm requires path to be tracked or added; use add -A as fallback
        try {
          await git.rm([rel]);
        } catch {
          await git.add(['-A']);
        }
        changed.add(rel);
      } else if (ch.action === 'rename' || ch.action === 'move') {
        const fromFull = ensureInsideRoot(this.projectRoot, ch.from);
        const toFull = ensureInsideRoot(this.projectRoot, ch.to);
        ensureDirForFile(toFull);
        if (fs.existsSync(fromFull)) {
          fs.renameSync(fromFull, toFull);
        } else {
          // If source doesn't exist, treat as write? Keep safety: create empty placeholder
          fs.writeFileSync(toFull, fs.existsSync(toFull) ? fs.readFileSync(toFull) : '', 'utf8');
        }
        const fromRel = toGitPath(path.relative(this.projectRoot, fromFull));
        const toRel = toGitPath(path.relative(this.projectRoot, toFull));
        // Stage rename by removing old and adding new
        try { await git.rm([fromRel]); } catch {}
        await git.add([toRel]);
        changed.add(fromRel);
        changed.add(toRel);
      }
    }

    this.appliedPaths.set(proposalId, changed);
    return { appliedPaths: Array.from(changed) };
  }

  async commitProposal(proposalId: ProposalId, message: string, metadata?: CommitMetadata): Promise<{ commit: string; branch: string | null }>
  {
    this.assertOnFeatureBranch();
    const git = this.git ?? (this.git = await getSimpleGit(this.projectRoot));
    const branch = this.branchName;

    const paths = this.appliedPaths.get(proposalId);
    if (!paths || paths.size === 0) {
      throw new Error('No applied changes to commit for this proposal');
    }

    let fullMessage = message;
    if (metadata && Object.keys(metadata).length > 0) {
      fullMessage += `\n\n[overseer-factory-metadata]: ${JSON.stringify(metadata)}`;
    }

    await git.commit(fullMessage, Array.from(paths));
    const head = (await git.revparse(['HEAD']))?.trim();

    if (this.store && this.runId && head) {
      const title = message.split('\n')[0] ?? message;
      const body = message.split('\n').slice(1).join('\n') || null;
      this.store.saveGitCommit(this.runId, { commitHash: head, branch, title, body });
    }

    return { commit: head, branch: branch ?? null };
  }

  async revertProposal(proposalId: ProposalId): Promise<{ reverted: string[] }>
  {
    const git = this.git ?? (this.git = await getSimpleGit(this.projectRoot));
    const paths = this.appliedPaths.get(proposalId);
    if (!paths || paths.size === 0) return { reverted: [] };

    const reverted: string[] = [];
    // Try modern restore first, then fall back to checkout/reset combo
    try {
      await git.raw(['restore', '--staged', '--worktree', '--source=HEAD', '--', ...Array.from(paths)]);
      reverted.push(...paths);
    } catch {
      // Fallback: unstage and checkout file versions from HEAD
      try {
        await git.reset(['HEAD', '--', ...Array.from(paths)]);
      } catch {}
      try {
        await git.checkout(['--', ...Array.from(paths)]);
      } catch {}
      reverted.push(...paths);
    }

    this.appliedPaths.delete(proposalId);
    return { reverted };
  }

  getActiveBranch(): string | null {
    return this.branchName;
  }

  getLastStashMessage(): string | null {
    return this.lastStashMessage;
  }
}
