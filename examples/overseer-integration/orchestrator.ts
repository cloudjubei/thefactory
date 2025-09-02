/*
 A minimal mock Orchestrator that simulates an agent run.
 It demonstrates how to emit events compatible with the factory-ts events API, and how a run would propose file changes.
 Replace this with the real orchestrator wired to the factory-ts library in your app.
*/

import type { RunHandle } from "../../packages/factory-ts/src/events/types";
import crypto from "node:crypto";

export interface LaunchOptions {
  llm: { provider: string; model: string; maxTokens?: number };
  budgetUsd?: number;
}

export class MockOrchestrator {
  private runs = new Map<string, Promise<void>>();
  constructor(private opts: { projectRoot: string; projectId: string; taskId: string }) {}

  launch(handle: RunHandle, options: LaunchOptions): string {
    const runId = crypto.randomUUID();

    const run = (async () => {
      const startTs = Date.now();
      handle.emit("run/start", {
        runId,
        timestamp: Date.now(),
        metadata: {
          projectId: this.opts.projectId,
          taskId: this.opts.taskId,
          projectRoot: this.opts.projectRoot,
          llm: options.llm,
          budgetUsd: options.budgetUsd,
        },
      });

      // Simulate progress
      for (const step of [
        "Analyzing task context",
        "Planning changes",
        "Drafting patch",
      ]) {
        await sleep(200);
        handle.emit("run/progress", { runId, timestamp: Date.now(), message: step });
        handle.emit("run/progress/snapshot", { runId, timestamp: Date.now(), tokensUsed: rand(200, 600), costUsd: Math.random() * 0.02 });
      }

      // Propose a file change (new file)
      const proposal = {
        baseDir: this.opts.projectRoot,
        changes: [
          {
            type: "write" as const,
            path: "examples/overseer-integration/hello.txt",
            before: null,
            after: "Hello from the Overseer integration example!\n",
          },
        ],
      };

      handle.emit("files/proposal", { runId, timestamp: Date.now(), proposal });

      // Wait to see if user accepts or rejects
      const decision = await waitForDecision(handle, runId);
      if (!decision.accepted) {
        handle.emit("run/end", { runId, timestamp: Date.now(), status: "rejected", durationMs: Date.now() - startTs });
        return;
      }

      // Simulate apply + commit
      await sleep(150);
      handle.emit("git/commit", { runId, timestamp: Date.now(), message: "feat: add hello example", branch: "feature/overseer-demo", commitSha: randomSha() });

      handle.emit("run/end", { runId, timestamp: Date.now(), status: "success", durationMs: Date.now() - startTs });
    })().catch((err) => {
      handle.emit("run/error", { runId, timestamp: Date.now(), error: { message: String(err?.message || err) } });
      handle.emit("run/end", { runId, timestamp: Date.now(), status: "error", durationMs: 0 });
    });

    this.runs.set(runId, run);
    return runId;
  }

  async waitForCompletion(runId: string): Promise<void> {
    const p = this.runs.get(runId);
    if (p) await p;
  }
}

function sleep(ms: number) {
  return new Promise((res) => setTimeout(res, ms));
}

function rand(min: number, max: number) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function randomSha() {
  return [...crypto.randomBytes(20)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

async function waitForDecision(handle: RunHandle, runId: string) {
  return new Promise<{ accepted: boolean }>((resolve) => {
    const offAccept = handle.on("files/accept", (e) => {
      if (e.runId === runId) {
        offAccept();
        offReject();
        resolve({ accepted: true });
      }
    });
    const offReject = handle.on("files/reject", (e) => {
      if (e.runId === runId) {
        offAccept();
        offReject();
        resolve({ accepted: false });
      }
    });
  });
}
