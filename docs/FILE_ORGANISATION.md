# File Organisation

This document describes how files and directories are organised in this repository to keep the project navigable, consistent, and easy to evolve.

## Top-Level Directory Layout
- docs/: Project documentation and specifications.
  - docs/tasks/: Canonical task schema and examples.
  - docs/PROJECTS_GUIDE.md: How child projects under projects/ are managed.
  - docs/RUN_AGENT_CLI.md: Minimal usage documentation for the Node CLI bridge that streams JSONL events.
  - docs/OVERSEER_INTEGRATION.md: How Overseer consumes the Electron adapter to launch runs and subscribe to progress and diffs.
  - docs/CONFIGURATION.md: Central configuration for paths, provider keys, budgets, and default behaviors.
- scripts/: Executables and tools used by the agent and CI.
  - scripts/runAgent.ts: Node/TypeScript CLI to launch agents, subscribe to orchestrator events, and stream JSONL to stdout. Parses args like --project-id, --task-id, --feature-id, --llm-config, --budget, --db-path, and --project-root.
- tasks/: Per-task workspaces containing task metadata and tests.
  - tasks/{id}/task.json: Canonical task definition for a single task.
  - tasks/{id}/tests/: Deterministic tests validating each feature in the task.
- projects/: Child project configurations.
- packages/: JavaScript/TypeScript packages maintained in this repo.
  - packages/factory-ts/: TypeScript library for Overseer agent orchestration (build via tsup, ESM+CJS).
    - src/
      - index.ts: Public entry point exporting the library API.
      - adapters/
        - electronShim.ts: IPC-agnostic adapter exposing serializable events and utilities for JSONL streaming, EventSource-like consumption, and Observables.
      - config/: Centralized configuration resolver used by all modules.
        - index.ts: resolveConfig/getConfig/setConfig/applyRuntimeConfig APIs with env and default resolution.
      - events/: Typed run lifecycle event bus and RunHandle.
        - types.ts: IPC-serializable event payload types and EventBus/RunHandle interfaces. Includes error/retry events. Now includes 'run/truncated' event for transcript caps, and 'run/progress/snapshot' for periodic, coalesced progress updates.
        - runtime.ts: Lightweight typed event emitter and DefaultRunHandle implementation.
        - backpressure.ts: BufferedEventBus with async batching, bounded queue, drop/coalesce strategies, progress snapshot helper, and JSONL buffered streaming utility.
        - index.ts: Barrel export for events module.
      - errors/: Common, typed error utilities.
        - types.ts: FactoryError class, error codes, classification utilities, and conversions from unknown.
        - redact.ts: Configurable redaction helpers (configureRedaction, redactString, redactObject, deepRedact) and truncation utility (truncateString). Includes tests in errors/redact.test.ts.
      - files/: File change proposals and diffs (in-memory patchsets; no workspace mutation).
        - fileChangeManager.ts: Accepts proposed changes, validates path safety, and computes diffs.
        - sandboxOverlay.ts: Sandboxed filesystem overlay for safe writes before acceptance.
        - index.ts: Barrel export for files module.
      - git/: Git integration layer used by Overseer to manage feature branches and apply/commit/revert changes.
        - gitService.ts: Repo and commit helpers; records commit SHAs to the HistoryStore when provided.
        - index.ts: Barrel export for git module.
      - db/: Persistent run history (SQLite) module.
        - store.ts: HistoryStore convenience factory using centralized config.
      - artifacts/: Import/export of run archives for sharing and review.
        - types.ts: Archive schema (v1), export options, and imported run API.
        - recorder.ts: In-memory recorder that subscribes to a RunHandle and captures events, proposals, commits, usage, and metadata. Enforces transcript size limits and inserts 'run/truncated' marker events when caps are exceeded.
        - recorder.test.ts: Tests for recorder behavior.
        - exporter.ts: exportRun(runId, options) produces a redacted JSON archive with optional file snapshots and size limits; uses deepRedact.
        - importer.ts: importRun(filePath) validates and loads an archive and can replay events.
- examples/: Developer-facing runnable examples and integration references.
  - examples/overseer-integration/: Minimal Node/Electron-like mock demonstrating how to launch a run, subscribe to events, present diffs, and accept changes. Includes a React hook useAgentRun.

Notes:
- The TypeScript implementation (packages/factory-ts and scripts/runAgent.ts) is the primary orchestration path.
- Python entrypoints (run.py, scripts/run_local_agent.py) are deprecated and now print a deprecation banner. They will attempt to bridge to the Node CLI automatically when available and otherwise fall back to the legacy Python flow.
- Use env flags FACTORY_FORCE_PYTHON=1 or FACTORY_BRIDGE_TO_NODE=0 to disable auto-bridge.

## File Naming Conventions
- Tasks and features:
  - Task directories are numeric IDs: tasks/{id}/ (e.g., tasks/1/).
  - Tests are named per-feature: tasks/{task_id}/tests/test_{task_id}_{feature_number}.py (e.g., tasks/15/tests/test_15_3.py).
- Python modules: snake_case.py (e.g., task_format.py, run_local_agent.py).
- Documentation files: UPPERCASE or Title_Case for project-wide specs (e.g., TESTING.md, FILE_ORGANISATION.md). Place task-related docs under docs/tasks/.
- Javascript/TypeScript modules: camelCase.js/ts (e.g., taskFormat.js, runLocalAgent.ts).
- JSON examples/templates: Use .json with clear, descriptive names (e.g., task_example.json).

## Evolution Guidance
- Make minimal, incremental changes that are easy to review and test.
- Keep documentation authoritative: update docs first when changing schemas or protocols.
- Introduce shared utilities only when multiple tasks need them; otherwise keep helpers local to a task.
- Deprecate gradually: create new files/specs alongside old ones, migrate, then remove deprecated artifacts when tests prove stability.
- Each feature must have deterministic tests; do not mark features complete until tests pass.

## Example Tree (illustrative)
The following tree is graphical and illustrative of a typical repository layout:

```
repo_root/
├─ .env
├─ .gitignore
├─ LICENSE
├─ requirements.txt
├─ run.py
├─ docs/
│  ├─ AGENT_COMMUNICATION_PROTOCOL.md
│  ├─ AGENT_CONTEXTER.md
│  ├─ AGENT_DEVELOPER.md
│  ├─ AGENT_PLANNER.md
│  ├─ agent_response_example.json
│  ├─ AGENT_TESTER.md
│  ├─ FILE_ORGANISATION.md
│  ├─ LOCAL_SETUP.md
│  ├─ PROJECTS_GUIDE.md
│  ├─ RUN_AGENT_CLI.md
│  └─ OVERSEER_INTEGRATION.md
├─ scripts/
│  ├─ child_project_utils.py
│  ├─ git_manager.py
│  ├─ run_local_agent.py
│  ├─ run_tests.py
│  └─ runAgent.ts
├─ projects/
│  └─ child-project-1.json
├─ packages/
│  └─ factory-ts/
│     ├─ package.json
│     └─ src/
│        ├─ index.ts
│        ├─ adapters/
│        │  └─ electronShim.ts
│        ├─ config/
│        │  └─ index.ts
│        ├─ events/
│        │  ├─ index.ts
│        │  ├─ runtime.ts
│        │  ├─ types.ts
│        │  └─ backpressure.ts
│        ├─ review/
│        │  └─ reviewService.ts
│        ├─ files/
│        │  ├─ fileChangeManager.ts
│        │  ├─ sandboxOverlay.ts
│        │  ├─ index.ts
│        │  └─ *.test.ts
│        ├─ git/
│        │  ├─ gitService.ts
│        │  └─ index.ts
│        ├─ db/
│        │  └─ store.ts
│        ├─ errors/
│        │  ├─ types.ts
│        │  ├─ redact.ts
│        │  └─ redact.test.ts
│        └─ artifacts/
│           ├─ types.ts
│           ├─ recorder.ts
│           ├─ recorder.test.ts
│           ├─ exporter.ts
│           └─ importer.ts
└─ examples/
   └─ overseer-integration/
      ├─ README.md
      ├─ tsconfig.json
      ├─ index.ts
      ├─ orchestrator.ts
      └─ diffPresenter.ts
```

This update notes that Python entrypoints are now deprecated and bridged to the Node CLI.
