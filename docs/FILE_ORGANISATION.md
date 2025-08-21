# File Organisation

This document outlines the file and directory structure for the project, providing a clear scheme for organising all artifacts.

## Top-Level Directory Layout

The repository is structured to separate documentation, application source code, scripts, and task-specific files.

-   `/docs`: Contains all project documentation, including specifications, guidance, and architectural documents.
-   `/scripts`: Holds utility scripts for development, testing, and automation.
    -   `/scripts/tools`: Contains Python modules that implement the tools available to the agent.
-   `/src`: Reserved for the primary source code of the application (if any). *Currently unused.*
-   `/tasks`: The core directory for all task-related artifacts. Each task has its own subdirectory.
    -   `/tasks/{task_id}/`: A directory for a specific task.
        -   `task.json`: The canonical definition of the task and its features.
        -   `/tests/`: Contains test files for the features of this task.

## File Naming Conventions

-   **Task Definition Files**: `tasks/{task_id}/task.json`
-   **Test Files**: `tasks/{task_id}/tests/test_{task_id}_{feature_number}.py` (e.g., `test_1_5.py` for feature 1.5).
-   **Documentation**: Markdown files should use `UPPERCASE_SNAKE_CASE.md` (e.g., `FILE_ORGANISATION.md`).
-   **Python Scripts**: Python files should use `lowercase_snake_case.py`.

## Evolution Guidance

This structure is designed to be extensible.
-   New top-level directories should be added only for entirely new categories of artifacts (e.g., a `/data` directory for datasets).
-   Changes to the core structure, especially within `/tasks`, must be reflected in the project's documentation (`docs/tasks/TASKS_GUIDANCE.md`) and tooling (`scripts/tools/task_utils.py`).
-   The principle is to keep related items co-located, especially for tasks, where the definition and its tests live under the same parent directory.

## Example Tree

Here is an illustrative tree of the repository structure:

```
.
├── docs
│   ├── AGENT_PRINCIPLES.md
│   ├── FILE_ORGANISATION.md
│   ├── PLAN_SPECIFICATION.md
│   ├── TESTING.md
│   ├── TOOL_ARCHITECTURE.md
│   └── tasks
│       ├── TASKS_GUIDANCE.md
│       ├── task_example.json
│       └── task_format.py
├── scripts
│   ├── run_local_agent.py
│   ├── run_tests.py
│   └── tools
│       ├── ask_question.py
│       ├── ...
│       └── write_file.py
├── tasks
│   └── 1
│       ├── task.json
│       └── tests
│           └── test_1_5.py
└── .gitignore
```