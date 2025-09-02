# Node CLI Bridge: runAgent.ts

This repository provides a Node/TypeScript CLI (scripts/runAgent.ts) to launch agents and stream JSONL events to stdout. While Overseer integrates directly via the Electron adapter, this CLI remains for backward compatibility and debugging.

Basic usage:

- --project-id: The project configuration ID
- --task-id: Task ID to run
- --feature-id: Optional feature ID
- --llm-config: JSON string or path for the LLM provider configuration
- --budget: Max USD budget for the run
- --db-path: Optional path to SQLite DB for run history
- --project-root: Path to the project root where files will be read/written

Output protocol: Each line is a JSON event matching packages/factory-ts/src/events/types.ts (RunEvent).

The Electron adapter uses the same serializable event shapes for IPC.
