# File Organisation

This document outlines the standard directory structure and naming conventions for files within this repository. Adhering to this structure ensures consistency, predictability, and ease of navigation.

## Directory Structure

The repository is organized into the following top-level directories:

-   **/docs**: Contains all specification documents, guides, and long-form markdown documentation. This includes `SPEC.md`, architectural decisions, and user guides.
-   **/scripts**: Contains all executable scripts, primarily the agent's orchestrator.
-   **/plans**: Contains the execution plans for each task.
-   **/tests**: Contains test suites for the project's components.
-   **/**: The root directory is reserved for project management files (`TASKS.md`), configuration (`.env.example`, `requirements.txt`), and essential markers (`README.md`, `.gitignore`).

### Detailed Structure

```
.
├── .env.example
├── .gitignore
├── README.md
├── TASKS.md
├── requirements.txt
├── docs/
│   ├── AGENT_PRINCIPLES.md
│   ├── FILE_ORGANISATION.md
│   ├── LOCAL_SETUP.md
│   ├── PLAN_SPECIFICATION.md
│   ├── SPEC.md
│   ├── SPECIFICATION_GUIDE.md
│   ├── TASK_FORMAT.md
│   ├── TEMPLATE.md
│   └── TOOL_ARCHITECTURE.md
├── plans/
│   └── ... (task plans)
└── scripts/
    └── run_local_agent.py
```

## Naming Conventions

-   **Directories**: `lower-kebab-case`
-   **Markdown Files**: `UPPER_SNAKE_CASE.md`. This convention applies to all core specification and documentation files.
-   **Scripts**: `lower_snake_case.py`.
-   **Configuration Files**: Use standard names for the technology (e.g., `requirements.txt`, `.gitignore`).

## Adherence Plan

To align the current repository with this specification, the following files must be moved. This refactoring requires agent tools for moving and deleting files, which are not yet implemented.

**Files to Move:**

- `AGENT_PRINCIPLES.md` -> `docs/AGENT_PRINCIPLES.md`
- `LOCAL_SETUP.md` -> `docs/LOCAL_SETUP.md`
- `PLAN_SPECIFICATION.md` -> `docs/PLAN_SPECIFICATION.md`
- `SPEC.md` -> `docs/SPEC.md`
- `SPECIFICATION_GUIDE.md` -> `docs/SPECIFICATION_GUIDE.md`
- `TASK_FORMAT.md` -> `docs/TASK_FORMAT.md`
- `TEMPLATE.md` -> `docs/TEMPLATE.md`
- `TOOL_ARCHITECTURE.md` -> `docs/TOOL_ARCHITECTURE.md`

A dedicated task has been created to perform this refactoring once the necessary tools are available.
