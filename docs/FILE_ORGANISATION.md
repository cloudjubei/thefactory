# File Organisation

This document describes how files and directories are organised in this repository to keep the project navigable, consistent, and easy to evolve.

## Top-Level Directory Layout
- docs/: Project documentation and specifications.
  - docs/tasks/: Canonical task schema and examples.
  - docs/PROJECTS_GUIDE.md: How child projects under projects/ are managed.
  - docs/RUN_AGENT_CLI.md: Minimal usage documentation for the Node CLI bridge that streams JSONL events.
  - docs/OVERSEER_INTEGRATION.md: How Overseer consumes the Electron adapter to launch runs and subscribe to progress and diffs.
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
      - events/: Typed run lifecycle event bus and RunHandle.
        - types.ts: IPC-serializable event payload types and EventBus/RunHandle interfaces. Includes error/retry events.
        - runtime.ts: Lightweight typed event emitter and DefaultRunHandle implementation.
        - index.ts: Barrel export for events module.
      - errors/: Common, typed error utilities.
        - types.ts: FactoryError class, error codes, classification utilities, and conversions from unknown.
        - redact.ts: Safe redaction helpers for messages and objects.
      - files/: File change proposals and diffs (in-memory patchsets; no workspace mutation).
        - fileChangeManager.ts: Accepts proposed changes, validates path safety, and computes diffs.
        - sandboxOverlay.ts: Sandboxed filesystem overlay for safe writes before acceptance.
        - index.ts: Barrel export for files module.
      - git/: Git integration layer used by Overseer to manage feature branches and apply/commit/revert changes.
        - gitService.ts: Repo and commit helpers; records commit SHAs to the HistoryStore when provided.
        - index.ts: Barrel export for git module.
      - db/: Persistent run history (SQLite) module.
        - store.ts: HistoryStore convenience factory.

Notes:
- All changes should be localized to the smallest reasonable scope (task- or doc-specific) to reduce coupling.
- Documentation in docs/ is the single source of truth for specs and formats.

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
│        ├─ events/
│        │  ├─ index.ts
│        │  ├─ runtime.ts
│        │  └─ types.ts
│        ├─ review/
│        │  └─ reviewService.ts
│        ├─ files/
│        │  ├─ fileChangeManager.ts
│        │  ├─ sandboxOverlay.ts
│        │  └─ index.ts
│        ├─ git/
│        │  ├─ gitService.ts
│        │  └─ index.ts
│        ├─ db/
│        │  └─ store.ts
│        └─ errors/
│           ├─ types.ts
│           └─ redact.ts
└─ tasks/
   ├─ 1/
   │  ├─ task.json
   │  └─ tests/
   │     └─ test_1_3.py
   └─ 2/
      ├─ task.json
      └─ tests/
```

This diagram includes the Electron adapter under packages/factory-ts/src/adapters and the typed events/RunHandle infrastructure used by Overseer.
