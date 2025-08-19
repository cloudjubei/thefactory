# File Organisation

Authoritative reference: This document defines the repository file organization and is referenced by Task 3 in tasks/TASKS.md per the Non-Redundancy Principle. Tasks should reference this file rather than duplicating its details.

This document outlines the standard file and directory structure for the project. A consistent structure is essential for maintaining clarity, scalability, and ease of navigation as the project grows.

## Guiding Principles

- **Clarity over Brevity**: Directory and file names should be descriptive and unambiguous.
- **Logical Grouping**: Related files should be grouped together by function or type.
- **Scalability**: The structure should accommodate future growth without requiring major refactoring.

## Top-Level Directory Structure

```
.
├── .github/         # CI/CD workflows and issue templates
├── docs/            # All specification, guides, and documentation
├── scripts/         # Executable scripts (e.g., the Orchestrator)
├── src/             # Source code for project-specific libraries or modules (if any)
├── tasks/           # The main task list and per-task plan folders
├── tests/           # Automated tests
│
├── .env.example     # Template for environment variables
├── .gitignore       # Git ignore rules
├── LOCAL_SETUP.md   # User guide for local setup and execution
├── README.md        # High-level project overview and entry point
└── requirements.txt # Python package dependencies
```

## Directory Descriptions

- **`.github/`**: Contains GitHub-specific configuration, such as action workflows for continuous integration and testing.
- **`docs/`**: The central repository for all project documentation. This includes high-level specifications, technical guides, architectural documents, and principles.
  - Examples: `SPEC.md`, `TOOL_ARCHITECTURE.md`, `SPECIFICATION_GUIDE.md`.
- **`scripts/`**: Contains standalone, executable scripts. The primary example is the agent's Orchestrator.
  - Example: `run_local_agent.py`.
- **`src/`**: Reserved for Python source code that is not a standalone script but a module or library to be imported by other parts of the project.
- **`tasks/`**: Holds the project's task list and per-task plans.
  - `tasks/TASKS.md`: The canonical task list.
  - `tasks/{id}/plan_{id}.md`: The plan for task `{id}`, including its feature list.
- **`tests/`**: Contains all automated tests, including unit tests, integration tests, and end-to-end tests.

## File Naming Conventions

- **Documentation (`.md`)**: `UPPER_SNAKE_CASE.md`
  - Rationale: Distinguishes core specification documents as stable, important artifacts.
  - Example: `FILE_ORGANISATION.md`, `AGENT_PRINCIPLES.md`.
- **Python Scripts (`.py`)**: `lower_snake_case.py`
  - Rationale: Follows the standard Python PEP 8 style guide.
  - Example: `run_local_agent.py`.
- **Configuration Files**: Use standard names where applicable.
  - Example: `requirements.txt`, `.gitignore`.

## Future Evolution

This file structure is a living document. As the project evolves, it may be necessary to add new directories or adjust the organization. Any such changes should be proposed via a task and this document should be updated accordingly.
