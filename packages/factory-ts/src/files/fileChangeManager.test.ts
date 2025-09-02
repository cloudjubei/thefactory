import { describe, it, expect } from 'vitest';
import { FileChangeManager } from './fileChangeManager';
import path from 'node:path';
import fs from 'node:fs';
import os from 'node:os';

function makeTempProject() {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'factory-ts-proj-'));
  fs.mkdirSync(path.join(dir, 'src'));
  fs.writeFileSync(path.join(dir, 'src', 'hello.txt'), 'hello\nworld\n', 'utf8');
  return dir;
}

describe('FileChangeManager', () => {
  it('creates proposal and computes diff without mutating workspace', async () => {
    const root = makeTempProject();
    const mgr = new FileChangeManager({ projectRoot: root });

    const proposal = mgr.createProposal([
      { action: 'write', path: 'src/hello.txt', content: 'hello\nfriend\n' },
      { action: 'write', path: 'src/new.txt', content: 'new file\n' },
      { action: 'delete', path: 'src/hello.txt' }, // delete original (just to test multi changes)
    ]);

    expect(proposal.status).toBe('open');
    expect(fs.readFileSync(path.join(root, 'src', 'hello.txt'), 'utf8')).toBe('hello\nworld\n');

    const diff = await mgr.getProposalDiff(proposal.id);
    expect(typeof diff).toBe('string');
    expect(diff).toContain('src/hello.txt');
    expect(diff).toContain('src/new.txt');
  });

  it('emits events for proposal and diff', async () => {
    const root = makeTempProject();
    const mgr = new FileChangeManager({ projectRoot: root });

    let created = false;
    let diffed = false;
    mgr.on('file:proposal', (e) => { if (e.op === 'created') created = true; });
    mgr.on('file:diff', () => { diffed = true; });

    const proposal = mgr.createProposal([{ action: 'write', path: 'src/a.txt', content: 'A' }]);
    await mgr.getProposalDiff(proposal.id);

    expect(created).toBe(true);
    expect(diffed).toBe(true);
  });

  it('validates path safety', () => {
    const root = makeTempProject();
    const mgr = new FileChangeManager({ projectRoot: root });
    expect(() => mgr.createProposal([{ action: 'write', path: '../escape.txt', content: 'x' }])).toThrow();
  });
});
