/*
 Minimal Node/Electron-like launcher showcasing how Overseer might:
 - Launch a run using a mock orchestrator
 - Subscribe to events via factory-ts events API
 - Show diffs and accept changes

 This script is intentionally simple and focuses on wiring and developer ergonomics.
*/

import { DefaultRunHandle, createEventBus } from "../../packages/factory-ts/src/events/runtime";
import { BufferedEventBus } from "../../packages/factory-ts/src/events/backpressure";
import { MockOrchestrator } from "./orchestrator";
import { presentDiffAndPromptAccept } from "./diffPresenter";
import path from "node:path";
import readline from "node:readline";

async function prompt(question: string): Promise<string> {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  return new Promise((resolve) => rl.question(question, (ans) => { rl.close(); resolve(ans); }));
}

async function main() {
  // Project/task inputs (would come from Overseer UI)
  const projectRoot = path.resolve(process.cwd());
  const projectId = "example-project";
  const taskId = "example-task";

  // Event bus with buffering for responsive UIs
  const rawBus = createEventBus();
  const bus = new BufferedEventBus(rawBus, { maxQueue: 500, coalesceProgressMs: 150 });
  const handle = new DefaultRunHandle(bus);

  // Subscribe to events (UI would use these to update state)
  const unsub = [
    bus.on("run/start", (e) => console.log(`[run] start id=${e.runId} task=${e.metadata?.taskId}`)),
    bus.on("run/progress", (e) => console.log(`[run] progress: ${e.message}`)),
    bus.on("run/progress/snapshot", (e) => console.log(`[run] snapshot: tokens=${e.tokensUsed} cost=$${e.costUsd?.toFixed(4)}`)),
    bus.on("files/proposal", async (e) => {
      console.log("\n[files] proposal received:");
      const decision = await presentDiffAndPromptAccept(e.proposal);
      if (decision.accept) {
        console.log("[files] accepting changes...\n");
        handle.emit("files/accept", { runId: e.runId, accepted: e.proposal });
      } else {
        console.log("[files] rejected by user\n");
        handle.emit("files/reject", { runId: e.runId, rejected: e.proposal, reason: decision.reason || "user declined" });
      }
    }),
    bus.on("run/error", (e) => console.error("[run] error:", e.error?.message || e.error)),
    bus.on("run/end", (e) => console.log(`[run] end status=${e.status} durationMs=${e.durationMs}`)),
  ];

  // Launch the orchestrator run (this is a mock; swap with real one wired to factory-ts internals)
  const orchestrator = new MockOrchestrator({ projectRoot, projectId, taskId });
  const runId = orchestrator.launch(handle, {
    llm: { provider: "openai", model: "gpt-4o-mini", maxTokens: 2000 },
    budgetUsd: 0.10,
  });

  console.log(`\nLaunched run ${runId}. Streaming events...`);
  await orchestrator.waitForCompletion(runId);

  // Keep console open if user wants to review logs
  const ans = await prompt("\nPress Enter to exit... ");
  unsub.forEach((fn) => fn());
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
