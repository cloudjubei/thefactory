/*
 A tiny presenter that prints a unified diff for proposed changes and asks the user if they want to accept.
 This uses a minimal formatting to avoid extra dependencies. Integrate with your UI in Overseer.
*/

import fs from "node:fs";
import path from "node:path";

export interface FileChange {
  type: "write" | "delete" | "rename" | "move";
  path: string;
  before: string | null;
  after: string | null;
}

export interface Proposal {
  baseDir: string;
  changes: FileChange[];
}

export async function presentDiffAndPromptAccept(proposal: Proposal): Promise<{ accept: boolean; reason?: string }> {
  console.log("Proposed changes:\n");
  for (const c of proposal.changes) {
    const abs = path.join(proposal.baseDir, c.path);
    const before = c.before ?? (fs.existsSync(abs) ? fs.readFileSync(abs, "utf8") : "");
    const after = c.after ?? "";

    console.log(`--- a/${c.path}`);
    console.log(`+++ b/${c.path}`);

    const diff = simpleUnifiedDiff(before, after);
    for (const line of diff) console.log(line);
    console.log("");
  }

  const answer = await askYesNo("Accept these changes? [y/N] ");
  return { accept: answer };
}

function askYesNo(q: string): Promise<boolean> {
  return new Promise((resolve) => {
    process.stdout.write(q);
    process.stdin.resume();
    process.stdin.setEncoding("utf8");
    const onData = (chunk: string) => {
      process.stdin.pause();
      process.stdin.removeListener("data", onData);
      const ans = (chunk || "").trim().toLowerCase();
      resolve(ans === "y" || ans === "yes");
    };
    process.stdin.on("data", onData);
  });
}

// Very naive unified diff for demonstration only.
function simpleUnifiedDiff(a: string, b: string): string[] {
  const aLines = a.split(/\r?\n/);
  const bLines = b.split(/\r?\n/);
  const max = Math.max(aLines.length, bLines.length);
  const out: string[] = [];
  for (let i = 0; i < max; i++) {
    const left = aLines[i] ?? "";
    const right = bLines[i] ?? "";
    if (left === right) {
      out.push(" " + left);
    } else {
      if (left) out.push("-" + left);
      if (right) out.push("+" + right);
    }
  }
  return out;
}
