# File Organisation Specification

## 1. Purpose
This document outlines the standard file and directory structure for the repository. A consistent structure is essential for locating files, understanding the project's architecture, and automating processes.

## 2. Top-Level Directory Layout
- `docs/`: Contains all project documentation, including specifications, guides, and architectural diagrams.
- `scripts/`: Holds automation and utility scripts. This includes the agent orchestrator, testing tools, and any other scripts needed for development and execution.
- `tasks/`: The central location for all task-related files. This directory is the primary workspace for the AI agent.
- `.github/`: Contains GitHub-specific files, primarily for CI/CD workflows.

## 3. `docs/` Directory
This directory houses all specification documents that define the agent's behavior and the project's standards.
- `SPEC.md`: The main specification document.
- `AGENT_PRINCIPLES.md`: Core principles guiding the agent's operation.
- `PLAN_SPECIFICATION.md`: Defines the structure and requirements for an agent's plan.
- `FEATURE_FORMAT.md`: Details the format for defining features within a plan.
- `FILE_ORGANISATION.md`: This file.
- `TESTING.md`: Specification for writing and running tests.
- `TOOL_ARCHITECTURE.md`: Describes the available tools and the agent's interaction with them.

## 4. `scripts/` Directory
This directory contains all executable scripts.
- `run_local_agent.py`: The main orchestrator for running the agent locally.
- `run_tests.py`: The test runner script invoked by the `run_tests` tool.
- `tools/`: A subdirectory for individual tool implementations (e.g., `submit_for_review.py`).

## 5. `tasks/` Directory
This is the most critical directory for the agent's day-to-day work.
- `tasks/{task_id}/task.json`: A JSON file that serves as the single source of truth for a task's definition, including its plan, acceptance criteria, and features.
- `tasks/{task_id}/tests/`: A directory containing all tests for the corresponding task. Each test file should be named `test_{feature_id}.py`.

## 6. File Naming Conventions
- Specification documents: PascalCase (e.g., `PLAN_SPECIFICATION.md`).
- Scripts: snake_case (e.g., `run_local_agent.py`).
- Test files: `test_{feature_id}.py` (e.g., `test_13_1.py`).
- Task definition files: `task.json`.

## 7. Evolution Guidance
This file organisation is not static. Any changes to the structure must be proposed and documented in a task. Major changes should be reflected in this document. The goal is to maintain clarity and predictability as the project evolves.
