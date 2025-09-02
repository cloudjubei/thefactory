# File Organisation

This document describes how files and directories are organised in this repository to keep the project navigable, consistent, and easy to evolve.

## Top-Level Directory Layout
- docs/: Project documentation and specifications.
  - docs/tasks/: Canonical task schema and examples.
  - docs/PROJECTS_GUIDE.md: How child projects under projects/ are managed.
- scripts/: Executables and tools used by the agent and CI.
- tasks/: Per-task workspaces containing task metadata and tests.
  - tasks/{id}/task.json: Canonical task definition for a single task.
  - tasks/{id}/tests/: Deterministic tests validating each feature in the task.
- projects/: Child project configurations.
- packages/: JavaScript/TypeScript packages maintained in this repo.
  - packages/factory-ts/: TypeScript library for Overseer agent orchestration (build via tsup, ESM+CJS).
    - src/
      - index.ts: Public entry point exporting the library API.
      - orchestrator.ts: Orchestrator API exposing runTask and runFeature that wire loaders, LLM client, and the typed event bus. Returns a RunHandle, supports cancellation with AbortController.
      - events/: Typed run lifecycle event bus and RunHandle.
        - types.ts: IPC-serializable event payload types and EventBus/RunHandle interfaces.
        - runtime.ts: Lightweight typed event emitter and DefaultRunHandle implementation.
        - index.ts: Barrel export for events module.
      - llm/: Provider-agnostic LLM client interfaces and adapters.
        - types.ts: Core types (LLMClient, streaming, usage, costs utils).
        - config.ts: Overseer LLMConfig and normalization helpers.
        - costs.ts: Model cost tables (OpenAI to start).
        - openaiClient.ts: OpenAI adapter using official SDK (dynamic import).
        - factory.ts: makeLLMClient that adapts LLMConfig -> LLMClient and supports DI.
      - telemetry/: Telemetry and budgets.
        - telemetry.ts: Tracks token usage (prompt/completion), requests, duration timestamps, and computes costs from provider pricing (OpenAI). Supports streaming updates and budget enforcement with AbortController and typed events.
      - domain.ts: Zod schemas and types for ProjectConfig and TaskDefinition.
      - utils/path.ts: Cross-platform path helpers, root resolution.
      - loaders/projectLoader.ts: Project and task loader with validation.
      - loaders/projectLoader.test.ts: Vitest tests for the loader.
      - db/: Persistent run history (SQLite) module.
        - sqlite.ts: DB connection, migrations runner, and HistoryStore implementation.
        - store.ts: Convenience factory for creating the store with an opened DB handle.
        - migrations/
          - 0001_init.sql: Initial schema for runs, steps, messages, usage, file proposals, and git commit metadata.
      - files/: File change proposals and diffs (in-memory patchsets; no workspace mutation).
        - fileChangeManager.ts: Accepts proposed changes (writes/renames/deletes), validates path safety under a project root, and computes diffs against the working tree using git plumbing when available (git diff --no-index), with a simple unified diff fallback. Exposes API createProposal, getProposalDiff, updateProposal, discardProposal, and emits file:proposal and file:diff events.
        - index.ts: Barrel export for files module.
      - git/: Git integration layer used by Overseer to manage feature branches and apply/commit/revert changes.
        - gitService.ts: Provides ensureRepo, createFeatureBranch(runId), applyProposalToBranch(proposalId), commitProposal(proposalId, message, metadata), revertProposal(proposalId). It uses simple-git (dynamic import) and records commit SHAs to the HistoryStore when provided.
        - index.ts: Barrel export for git module.
      - review/: Change review workflow high-level APIs bridging files, git, and history.
        - reviewService.ts: Exposes listProposalFiles(proposalId), acceptAll(proposalId), acceptFiles(proposalId, files[]), rejectFiles(proposalId, files[]), rejectAll(proposalId). Provides per-file diff hunks and summary counts (added/modified/deleted). On accept, commits using gitService and records commit in HistoryStore; on reject, updates proposal state and history without workspace mutation.

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
│  └─ tasks/
│     ├─ task_format.py
│     └─ task_example.json
├─ scripts/
│  ├─ child_project_utils.py
│  ├─ git_manager.py
│  ├─ run_local_agent.py
│  ├─ run_tests.py
│  └─ task_utils.py
├─ projects/
│  └─ child-project-1.json
├─ packages/
│  └─ factory-ts/
│     ├─ package.json
│     └─ src/
│        ├─ index.ts
│        ├─ review/
│        │  └─ reviewService.ts
│        ├─ files/
│        │  ├─ fileChangeManager.ts
│        │  └─ index.ts
│        ├─ git/
│        │  ├─ gitService.ts
│        │  └─ index.ts
│        └─ db/
│           └─ store.ts
└─ tasks/
   ├─ 1/
   │  ├─ task.json
   │  └─ tests/
   │     └─ test_1_3.py
   └─ 2/
      ├─ task.json
      └─ tests/
```

This diagram includes the new review/ module, which centralizes the change review workflow and exposes APIs used by Overseer to present and resolve proposed file changes within its UI.
