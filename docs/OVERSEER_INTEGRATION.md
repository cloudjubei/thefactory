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

## Performance and Backpressure

High-frequency events (token streams, progress spam) can overwhelm the UI. Use the buffered bus and snapshots to keep the UI responsive:

- BufferedEventBus: async batching with bounded queues and drop/coalesce strategies.
- Coalescing: by default, run/progress and run/usage are coalesced within a short window.
- Truncation markers: when drops occur, a run/truncated event is inserted for transparency.
- Progress snapshots: subscribe to run/progress/snapshot for periodic, high-level updates at a fixed cadence.

Example wiring in Electron main:

```ts
import { electronShim, events } from 'factory-ts';

function createRunFromTask(params): events.RunHandle { /* your orchestrator */ throw new Error('wire me'); }

ipcMain.handle('factory/run/start', async (evt, args) => {
  const run = createRunFromTask(args);

  // Wrap with buffered bus for smoother streaming to renderer
  const buffered = new events.BufferedEventBus({
    maxQueueSize: 1000,
    maxQueueBytes: 500_000,
    flushIntervalMs: 16,
    dropStrategy: 'coalesce',
  });

  const unsubscribe = run.onEvent((e) => buffered.emit(e));
  const unsubBridge = electronShim.bridgeToSender({ on: (l) => buffered.on(l) }, 'factory/run/event', (channel, payload) => {
    evt.sender.send(channel, payload);
  });

  evt.sender.once('destroyed', () => { unsubscribe(); unsubBridge(); });
  return { runId: run.id };
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

The adapter can expose a JSONL stream of events, suitable for piping to logs or devtools. Use streamJSONLBuffered to avoid unbounded memory growth.

```ts
import { events } from 'factory-ts';
const stream = events.streamJSONLBuffered(runHandle);
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
- Backpressure handling is configurable; choose strategies that match your UI's needs.
