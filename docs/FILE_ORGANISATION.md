# File Organisation Specification

This document defines how files and directories are structured, named, and evolved in this repository to support specification-driven, tool-using agent workflows.

## Top-Level Directory Layout

A concise overview of the repository's root structure and the purpose of each directory.

- docs/
  - Project-wide specifications, guides, and reference documents.
  - Examples: PLAN_SPECIFICATION.md, TESTING.md, TOOL_ARCHITECTURE.md, AGENT_EXECUTION_CHECKLIST.md.
- tasks/
  - Task-scoped definitions and tests. Each task has its own folder: `tasks/{task_id}/`.
  - Inside each task folder:
    - `task.json` — the canonical definition for the task, its plan, and its features.
    - `tests/` — tests validating the features of this task.
- scripts/
  - Orchestrator, tools, and execution helpers for the agent runtime.
  - Example: scripts/run_local_agent.py, scripts/tools/*.
- projects/ (optional, may not exist yet)
  - Holds child projects/submodules if/when introduced as per CHILD_PROJECTS_SPECIFICATION.
- .github/ (optional)
  - CI/CD workflows and repository automation.
- Other top-level files
  - README.md, LICENSE, .gitignore, environment/config files as needed.

Example tree (illustrative):

```
/ (repo root)
├── docs/
│   ├── PLAN_SPECIFICATION.md
│   ├── TESTING.md
│   └── TOOL_ARCHITECTURE.md
├── tasks/
│   └── 3/
│       ├── task.json
│       └── tests/
│           └── test_3_2.py
├── scripts/
│   ├── run_local_agent.py
│   └── tools/
│       └── ...
└── .gitignore
```

## File Naming Conventions

Consistent naming improves discoverability and automates tooling.

- Markdown specifications (docs/)
  - Use UPPER_SNAKE_CASE with .md extension for primary specs and guides.
  - Examples: PLAN_SPECIFICATION.md, TESTING.md, TOOL_ARCHITECTURE.md.
- Task definitions and tests (`tasks/{task_id}/`)
  - Task definition filename: `task.json`.
  - Test filenames: `test_{task_id}_{feature_number}.py` (e.g., test_3_2.py).
  - Tests reside under `tasks/{task_id}/tests/`.
- Python scripts and modules (scripts/ and subdirs)
  - Use snake_case.py for modules (e.g., run_local_agent.py, write_file.py).
  - Packages use snake_case directories; tools live under scripts/tools/.
- General rules
  - Prefer ASCII, lowercase (except docs’ spec files, which are uppercase), hyphens or underscores for separators.
  - Be explicit and descriptive; avoid abbreviations unless well-established.
  - One logical entity per file (e.g., one task definition per `task.json`).

## Evolution Guidance

How to evolve the structure safely as the project grows.

- Plan changes
  - Reflect structural updates in relevant docs (e.g., this file) and task definitions.
  - When introducing new directories (e.g., projects/), document purpose and conventions.
- Safe refactors
  - Use repository tooling (e.g., rename_files) to move/rename files atomically.
  - Update references in specs and tests in the same change.
- Testing and verification
  - Add or update tests under `tasks/{task_id}/tests/` that assert new or changed conventions.
  - Run the test suite (run_tests) to ensure no regressions.
- Versioning and traceability
  - Make small, incremental changes; one feature per commit using finish_feature.
  - Clearly describe rationale and impact in commit messages and notes.
- Backwards compatibility
  - When breaking changes are necessary, provide migration notes and update affected tasks/features accordingly.

This specification should be revisited as repository needs evolve. Keep conventions simple, explicit, and enforceable via tests.
