# File Organisation Specification

This document outlines the standard file and directory structure for this repository. Adhering to this structure ensures consistency and predictability.

## 1. Top-Level Directory Layout

-   **/docs**: Contains all project documentation, including specifications, guidance, and architecture documents.
    -   **/docs/tasks**: Specific documentation related to the task management system (e.g., format, guidance, examples).
-   **/scripts**: Holds automation and utility scripts.
    -   **/scripts/tools**: Contains the implementations of tools available to the AI agent.
-   **/tasks**: The core directory for all tasks. Each task has its own subdirectory.
    -   **/tasks/{task_id}**: A directory for a specific task.
        -   `task.json`: The canonical definition, plan, and status for the task and its features.
        -   **/tests**: Contains test files for the features of this task.

## 2. File Naming Conventions

-   **Task Definition File**: `tasks/{task_id}/task.json`
-   **Test Files**: `tasks/{task_id}/tests/test_{task_id}_{feature_id}.py`. For example, the test for feature 1.2 would be `tasks/1/tests/test_1_2.py`.
-   **Documentation**: Files in `/docs` should have clear, descriptive names in uppercase with underscores, e.g., `PLAN_SPECIFICATION.md`.
-   **Python Scripts**: Use snake_case for Python filenames, e.g., `run_local_agent.py`.

## 3. Evolution Guidance

This structure is intended to be stable but can evolve. Any proposed changes to the top-level structure or core naming conventions should be discussed and implemented as a dedicated task. The goal is to maintain a logical and scalable organisation as the project grows. All changes must be reflected in this document.
