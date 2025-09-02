# Overseer Integration Guide

This guide explains how to integrate the factory-ts library into Overseer (Electron + React) and includes a runnable example under examples/overseer-integration.

Key goals:
- Launch agent runs from Overseer
- Stream progress and usage events
- Collect comprehensive run history and artifacts
- Present file change proposals and allow accept/reject
- Use Git feature branches for acceptance (example uses a mock commit)

Quick start with the example:
- See examples/overseer-integration/README.md

Core concepts:
- Event bus: Use the events runtime and buffered bus for responsive UIs
- RunHandle: Single subscription and emit surface for a run
- Files: Proposals and diffs are emitted as events; acceptance is signaled via files/accept
- Recorder/Artifacts: Subscribe to the run to record a shareable archive (not shown in the minimal example)

React hook useAgentRun:
- Found at examples/overseer-integration/useAgentRun.ts
- Provides state and actions for UI to render progress and accept/reject diffs

IPC in Electron:
- In production, bridge RunHandle events through IPC (main <-> renderer). The electronShim in factory-ts provides shapes that are serializable for this purpose.

Next steps for full integration:
- Replace MockOrchestrator with the real factory-ts orchestrator that performs task execution
- Wire Git operations via packages/factory-ts/src/git/gitService
- Record runs using packages/factory-ts/src/artifacts/recorder and exporter
- Add redaction around secrets using packages/factory-ts/src/errors/redact
