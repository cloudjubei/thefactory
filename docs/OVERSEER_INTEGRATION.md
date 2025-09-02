# Overseer Integration Adapter (Electron Shim)

This document describes how Overseer (Electron, TypeScript, React + Vite) can launch agents, subscribe to progress, and display diffs using the factory-ts library. The adapter is IPC-agnostic and only exposes serializable events and utilities that fit Electron's IPC patterns.

Key goals:
- Launch agents/runs from Overseer.
- Stream progress, usage, and file change proposals.
- Review diffs and accept/reject changes (git integration in core services; UI-driven via events and service calls).
- Persist rich run history via the HistoryStore (db module) if desired.

## Concepts

- RunHandle: Represents a running agent/task. Provides onEvent(listener), cancel(), and an id.
- RunEvent: Typed, IPC-serializable events for lifecycle, usage, errors, file proposals/diffs, and git commits.
- Adapter utilities: Convert RunHandle events into JSONL streams, EventSource-like streams, Observables, or bridge them to an IPC sender.

## Minimal Wiring in Electron

Example: main process creates a run and bridges events to renderer via ipcMain.

```ts
// main.ts (Electron main)
import { electronShim, events } from 'factory-ts';

// Assume createRun returns a RunHandle from your orchestrator.
function createRunFromTask(params): events.RunHandle { /* your orchestrator */ throw new Error('wire me'); }

ipcMain.handle('factory/run/start', async (evt, args) => {
  const run = createRunFromTask(args);
  const unsubscribe = electronShim.bridgeToSender(run, 'factory/run/event', (channel, payload) => {
    evt.sender.send(channel, payload); // relay to renderer
  });

  // Optional: cancel binding
  const webContentsId = evt.sender.id;
  const cleanup = () => { unsubscribe(); };
  evt.sender.once('destroyed', cleanup);

  return { runId: run.id };
});

ipcMain.handle('factory/run/cancel', async (_evt, { runId }) => {
  // Lookup your RunHandle by runId and call cancel()
});
```

Renderer consumption options:

```ts
// 1) EventSource-like
const source = electronShim.toEventSourceLike(runHandle);
source.addEventListener('*', (e) => console.log(e.type, e));
source.addEventListener('file/diff', (e) => renderDiffs(e.payload));

// 2) Observable (handy for React state)
const obs = electronShim.toObservable(runHandle);
const sub = obs.subscribe({ next: (e) => setState((s) => s.concat(e)) });

// 3) IPC listener (when bridged by main)
ipcRenderer.on('factory/run/event', (_e, event) => {
  // event is already serializable (plain JSON)
  handleEvent(event);
});
```

## JSONL Streaming

The adapter can expose a JSONL stream of events, suitable for piping to logs or devtools.

```ts
const stream = electronShim.streamJSONL(runHandle);
(async () => {
  for await (const line of stream) {
    process.stdout.write(line);
  }
})();
```

## Displaying Diffs and Review

Listen for file/proposal and file/diff events. Use the reviewService and gitService from factory-ts to accept or reject changes.

- file/proposal: a new proposal is created by the agent.
- file/diff: contains unified diffs per file and a summary.
- file/proposal-state: reflects accept/reject updates.
- git/commit: emitted after acceptance is committed to a feature branch.

Example UI flow in renderer:

1. When file/proposal arrives, show a proposal card with counts.
2. When file/diff arrives, render diff hunks (payload.files[]).
3. On Accept All: call reviewService.acceptAll(proposalId) via a main process bridge.
4. On Reject All/Files: call reviewService.rejectAll/ rejectFiles.
5. On accept, watch for git/commit to display commit SHA and update history.

## Notes

- The adapter contains no Electron-specific code. It only shapes data and consumption utilities.
- Use the db/store HistoryStore to persist runs, steps, and errors if you need historical views.
- For LLM usage and budgets, wire your orchestrator to emit run/usage and run/budget-exceeded events using the provided event types.
- Errors should be serialized via the adapter (message, code, stack) — avoid sending raw Error instances across IPC.
```
