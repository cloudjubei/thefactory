import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { spawnSync } from 'node:child_process';
import { EventEmitter } from 'node:events';

export type ProposalId = string;

export type FileWriteChange = { action: 'write'; path: string; content: string };
export type FileDeleteChange = { action: 'delete'; path: string };
export type FileRenameChange = { action: 'rename' | 'move'; from: string; to: string };
export type FileChange = FileWriteChange | FileDeleteChange | FileRenameChange;

export type ProposalStatus = 'open' | 'discarded';

export interface FileChangeProposal {
  id: ProposalId;
  projectRoot: string; // absolute, normalized
  createdAt: number;
  updatedAt: number;
  status: ProposalStatus;
  changes: FileChange[];
}

export type FileProposalEvent =
  | { type: 'file:proposal'; proposal: FileChangeProposal; op: 'created' | 'updated' | 'discarded' }
  | { type: 'file:diff'; proposalId: ProposalId; diff: string; when: number };

export interface FileChangeManagerOptions {
  projectRoot: string; // absolute path to the project root
}

function randomId(): string {
  return 'prop_' + Math.random().toString(36).slice(2, 10);
}

function normalizeAbs(p: string): string {
  return path.resolve(p);
}

function ensureInsideRoot(root: string, candidate: string): string {
  const full = path.resolve(root, candidate);
  const normalizedRoot = normalizeAbs(root);
  const rel = path.relative(normalizedRoot, full);
  if (rel.startsWith('..') || path.isAbsolute(rel)) {
    throw new Error(`Path escapes project root: ${candidate}`);
  }
  return full;
}

// Simple unified diff generator as a fallback when git is not available.
function simpleUnifiedDiff(oldStr: string | null, newStr: string | null, aPath: string, bPath: string): string {
  const aHeader = `--- a/${aPath}`;
  const bHeader = `+++ b/${bPath}`;
  if (oldStr == null && newStr == null) return `${aHeader}\n${bHeader}\n`; // nothing
  const oldLines = (oldStr ?? '').split(/\r?\n/);
  const newLines = (newStr ?? '').split(/\r?\n/);
  const max = Math.max(oldLines.length, newLines.length);
  const body: string[] = ['@@'];
  for (let i = 0; i < max; i++) {
    const a = oldLines[i];
    const b = newLines[i];
    if (a === b) {
      if (a !== undefined) body.push(` ${a}`);
    } else {
      if (a !== undefined) body.push(`-${a}`);
      if (b !== undefined) body.push(`+${b}`);
    }
  }
  return [aHeader, bHeader, ...body].join('\n') + '\n';
}

function tryGitDiff(oldContent: string | null, newContent: string | null, aPath: string, bPath: string): string | null {
  // Use git diff --no-index between temp files to produce a patch for a single change
  // If oldContent is null => compare /dev/null vs new
  // If newContent is null => compare old vs /dev/null
  // Otherwise compare old vs new
  const hasGit = spawnSync('git', ['--version'], { stdio: 'ignore' });
  if (hasGit.status !== 0) return null;

  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'factory-ts-diff-'));
  try {
    const aTmp = oldContent != null ? path.join(tmpDir, 'a.tmp') : '/dev/null';
    const bTmp = newContent != null ? path.join(tmpDir, 'b.tmp') : '/dev/null';

    if (oldContent != null) fs.writeFileSync(aTmp, oldContent, 'utf8');
    if (newContent != null) fs.writeFileSync(bTmp, newContent, 'utf8');

    const args = ['diff', '--no-index', '--patch', '--exit-code', '--', aTmp, bTmp];
    const res = spawnSync('git', args, { encoding: 'utf8' });
    // git diff returns 1 when there are differences, 0 when none, >1 on error
    if (res.status === 0 && res.stdout.trim() === '') {
      // No differences
      return `--- a/${aPath}\n+++ b/${bPath}\n`; // empty change
    }
    if (res.status === 1 || (res.status === 0 && res.stdout)) {
      // Adjust file headers to refer to the repo paths instead of temp paths
      const stdout = res.stdout.replace(/---\s+a\/.*\n\+\+\+\s+b\/.*\n/, `--- a/${aPath}\n+++ b/${bPath}\n`);
      return stdout;
    }
    return null;
  } catch {
    return null;
  } finally {
    try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch {}
  }
}

export class FileChangeManager {
  private projectRoot: string;
  private proposals = new Map<ProposalId, FileChangeProposal>();
  private emitter = new EventEmitter();

  constructor(opts: FileChangeManagerOptions) {
    this.projectRoot = normalizeAbs(opts.projectRoot);
    if (!fs.existsSync(this.projectRoot) || !fs.statSync(this.projectRoot).isDirectory()) {
      throw new Error(`projectRoot does not exist or is not a directory: ${this.projectRoot}`);
    }
  }

  on(event: 'file:proposal', listener: (e: Extract<FileProposalEvent, { type: 'file:proposal' }>) => void): () => void;
  on(event: 'file:diff', listener: (e: Extract<FileProposalEvent, { type: 'file:diff' }>) => void): () => void;
  on(event: FileProposalEvent['type'], listener: (e: FileProposalEvent) => void): () => void {
    this.emitter.on(event, listener);
    return () => this.emitter.off(event, listener);
  }

  private emit(evt: FileProposalEvent) {
    this.emitter.emit(evt.type, evt);
  }

  createProposal(changes: FileChange[]): FileChangeProposal {
    const id = randomId();
    const now = Date.now();
    const normalized = this.normalizeChanges(changes);
    const proposal: FileChangeProposal = { id, projectRoot: this.projectRoot, createdAt: now, updatedAt: now, status: 'open', changes: normalized };
    this.proposals.set(id, proposal);
    this.emit({ type: 'file:proposal', proposal, op: 'created' });
    return proposal;
  }

  updateProposal(id: ProposalId, changes: FileChange[]): FileChangeProposal {
    const p = this.proposals.get(id);
    if (!p) throw new Error(`Proposal not found: ${id}`);
    if (p.status !== 'open') throw new Error(`Cannot update proposal with status ${p.status}`);
    const normalized = this.normalizeChanges(changes);
    const updated: FileChangeProposal = { ...p, updatedAt: Date.now(), changes: normalized };
    this.proposals.set(id, updated);
    this.emit({ type: 'file:proposal', proposal: updated, op: 'updated' });
    return updated;
  }

  discardProposal(id: ProposalId): void {
    const p = this.proposals.get(id);
    if (!p) return; // idempotent
    if (p.status !== 'open') return;
    const updated: FileChangeProposal = { ...p, updatedAt: Date.now(), status: 'discarded' };
    this.proposals.set(id, updated);
    this.emit({ type: 'file:proposal', proposal: updated, op: 'discarded' });
  }

  getProposal(id: ProposalId): FileChangeProposal | undefined {
    return this.proposals.get(id);
  }

  async getProposalDiff(id: ProposalId): Promise<string> {
    const p = this.proposals.get(id);
    if (!p) throw new Error(`Proposal not found: ${id}`);
    // Build a combined patch text for all changes
    let combined = '';
    for (const ch of p.changes) {
      if (ch.action === 'write') {
        const full = ensureInsideRoot(this.projectRoot, ch.path);
        const oldContent = fs.existsSync(full) && fs.statSync(full).isFile() ? fs.readFileSync(full, 'utf8') : null;
        const aPath = ch.path;
        const bPath = ch.path;
        const git = tryGitDiff(oldContent, ch.content, aPath, bPath);
        combined += (git ?? simpleUnifiedDiff(oldContent, ch.content, aPath, bPath));
        if (!combined.endsWith('\n')) combined += '\n';
      } else if (ch.action === 'delete') {
        const full = ensureInsideRoot(this.projectRoot, ch.path);
        const oldContent = fs.existsSync(full) && fs.statSync(full).isFile() ? fs.readFileSync(full, 'utf8') : '';
        const aPath = ch.path;
        const bPath = ch.path;
        const git = tryGitDiff(oldContent, null, aPath, bPath);
        combined += (git ?? simpleUnifiedDiff(oldContent, null, aPath, bPath));
        if (!combined.endsWith('\n')) combined += '\n';
      } else {
        // rename/move: emit a minimal rename patch header; content unchanged
        const fromFull = ensureInsideRoot(this.projectRoot, ch.from);
        const toFull = ensureInsideRoot(this.projectRoot, ch.to);
        // Validate existence of source (optional)
        const existed = fs.existsSync(fromFull) && fs.statSync(fromFull).isFile();
        const header = `rename from ${ch.from}\nrename to ${ch.to}\n`;
        let content = header;
        if (existed) {
          // Attempt to show a pure rename patch with no content change
          const oldContent = fs.readFileSync(fromFull, 'utf8');
          const git = tryGitDiff(oldContent, oldContent, ch.from, ch.to);
          if (git) content = git; else content += simpleUnifiedDiff(oldContent, oldContent, ch.from, ch.to);
        }
        combined += content;
        if (!combined.endsWith('\n')) combined += '\n';
      }
    }
    this.emit({ type: 'file:diff', proposalId: id, diff: combined, when: Date.now() });
    return combined;
  }

  private normalizeChanges(changes: FileChange[]): FileChange[] {
    return changes.map((c) => {
      if ((c as any).action === 'write') {
        const { path: pth, content } = c as FileWriteChange;
        if (typeof pth !== 'string' || !pth.trim()) throw new Error('write.path must be a non-empty string');
        if (typeof content !== 'string') throw new Error('write.content must be a string');
        // validate inside root, but do not return absolute; keep relative for UX while storing
        ensureInsideRoot(this.projectRoot, pth);
        return { action: 'write', path: normSlash(pth), content };
      } else if ((c as any).action === 'delete') {
        const { path: pth } = c as FileDeleteChange;
        if (typeof pth !== 'string' || !pth.trim()) throw new Error('delete.path must be a non-empty string');
        ensureInsideRoot(this.projectRoot, pth);
        return { action: 'delete', path: normSlash(pth) };
      } else if ((c as any).action === 'rename' || (c as any).action === 'move') {
        const { from, to } = c as FileRenameChange;
        if (typeof from !== 'string' || !from.trim()) throw new Error('rename.from must be a non-empty string');
        if (typeof to !== 'string' || !to.trim()) throw new Error('rename.to must be a non-empty string');
        ensureInsideRoot(this.projectRoot, from);
        ensureInsideRoot(this.projectRoot, to);
        return { action: c.action, from: normSlash(from), to: normSlash(to) } as FileRenameChange;
      }
      throw new Error(`Unknown change action: ${(c as any).action}`);
    });
  }
}

function normSlash(pth: string): string {
  return pth.split(path.sep).join('/');
}

export default FileChangeManager;
