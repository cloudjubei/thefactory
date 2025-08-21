# Repository File Organisation Specification

This document defines how files and directories are structured in this repository so contributors can navigate, extend, and evolve it consistently.

# Top-Level Directory Layout

This section describes the purpose of each top-level folder and notable files.

- docs/
  - Project-wide documentation, specifications, and reference formats used by all personas.
  - Examples: task schemas, testing guidance, agent protocols.
- tasks/
  - Source of truth for tasks. Each task has its own folder with task.json and a tests/ subfolder for per-feature tests.
- scripts/
  - Orchestration code, tooling, and developer utilities (e.g., test runner, agent harness).
- .gitignore, README, configuration files
  - Standard project metadata and VCS configuration.

Guiding principle: documentation lives under docs/, automated tests per task live under tasks/{id}/tests/, and orchestration lives under scripts/.

# File Naming Conventions

Consistency improves discoverability. Use the following conventions:

- Tasks
  - Task definition: tasks/{task_id}/task.json
  - Tests per feature: tasks/{task_id}/tests/test_{task_id}_{feature_number}.py
    - Example: tasks/15/tests/test_15_3.py
- Documentation
  - Markdown specs: use UPPER_SNAKE_CASE for canonical documents (e.g., docs/TESTING.md, docs/FILE_ORGANISATION.md).
  - Task schema and examples live under docs/tasks/ (e.g., docs/tasks/task_format.py, docs/tasks/task_example.json).
- Python modules
  - snake_case.py for modules; TypedDict and schemas live in clearly named files (e.g., task_format.py).

# Evolution Guidance

The structure should evolve incrementally and intentionally:

- Backward compatibility: prefer additive changes; update specs and examples together.
- Single source of truth: schemas are authoritative (e.g., docs/tasks/task_format.py). Keep examples in sync.
- Locality: place new feature-specific assets within the owning task folder to reduce coupling.
- Testing-first: whenever adding documents or tools, create or update per-feature tests that assert required artifacts and content.
- Minimal surface: introduce shared utilities only when multiple tasks need them, and document rationale in docs/.

# Example tree (illustrative)

Below is a graphical, high-level view of the repository layout. This is illustrative, not exhaustive.

```
.
├── docs/
│   ├── FILE_ORGANISATION.md
│   ├── TESTING.md
│   └── tasks/
│       ├── task_format.py
│       └── task_example.json
├── scripts/
│   └── run_local_agent.py
└── tasks/
    └── 1/
        ├── task.json
        └── tests/
            └── test_1_3.py
```

Notes:
- Use this structure as a guide when adding new tasks, tests, and documentation.
- Keep examples and schemas synchronized to avoid drift.
