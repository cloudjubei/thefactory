# TASKS.md to JSON Migration Guide

This document outlines the step-by-step process for migrating the task management system from a single `tasks/TASKS.md` file to a structured, per-task JSON format (`tasks/{id}/task.json`).

## 1. Migration Plan

The migration will be executed in a phased approach to minimize disruption and ensure stability.

### Phase 1: Specification & Tooling (Features 13.1 - 13.6)
1.  **Define Schema:** A Python `TypedDict` schema will be created in `docs/tasks/task_format.py` to serve as the canonical data structure for tasks.
2.  **Create Tooling:** A utility module, `scripts/tools/task_utils.py`, will be developed to handle all CRUD (Create, Read, Update, Delete) operations for tasks, abstracting away direct file I/O.
3.  **Integrate with Orchestrator:** The main orchestrator (`run_local_agent.py`) will be updated to use the new tooling. A **dual-read mode** will be implemented to allow the agent to read tasks from both the old `TASKS.md` and the new `task.json` format simultaneously. This is crucial for a seamless transition.

### Phase 2: Migration Execution (Features 13.7 - 13.8)
1.  **Develop Migration Script:** A dedicated script, `scripts/migrate_tasks.py`, will be created. This script will:
    -   Parse `tasks/TASKS.md`.
    -   Parse each `tasks/{id}/plan_{id}.md` to extract features.
    -   Create a `tasks/{id}` directory for each task.
    -   Write the parsed data into `tasks/{id}/task.json`.
    -   Rename the plan file to `tasks/{id}/plan.md`.
    -   Move existing tests from `tasks/{id}/tests/test_{id}_{feature_id}.py` to the new location.
2.  **Execute and Validate:** The script will be run once to perform the migration. All project tests must pass after the migration to confirm its success.

### Phase 3: Cleanup (Features 13.9 - 13.10)
1.  **Remove Dual-Read Mode:** The backward-compatibility code in the orchestrator will be removed, making the JSON format the sole source of truth.
2.  **Deprecate `TASKS.md`:** The old `tasks/TASKS.md` file will be deleted from the repository.

## 2. Backward Compatibility Strategy

The **dual-read mode** is the core of our backward compatibility strategy. During the transition period (Phase 1 and 2), the system will function as follows:
-   **Read Operations:** When fetching a task, the orchestrator will first look for `tasks/{id}/task.json`. If not found, it will fall back to parsing `tasks/TASKS.md`.
-   **Write Operations:** All new tasks or updates will be written exclusively to the new JSON format. The `TASKS.md` file will be considered read-only and will not be updated once the migration script is run.

This ensures that the agent can continue to operate on existing tasks while new tasks and migrated tasks leverage the new system immediately.

## 3. Tooling Requirements

-   **`docs/tasks/task_format.py`:** Defines the data schema.
-   **`scripts/tools/task_utils.py`:** Provides functions for task manipulation (`get_task`, `update_task`, `create_task`). This becomes the single entry point for all task-related data operations.
-   **`scripts/migrate_tasks.py`:** A one-off script to perform the migration.

## 4. Rollback Plan

In the event of a critical failure during or after the migration, the following steps can be taken to revert the changes:

1.  **Revert the Migration Commit:** The simplest method is to use `git revert` on the commit that contains the migration changes (from running `scripts/migrate_tasks.py`).
2.  **Manual Reversion:** If a git revert is not feasible:
    -   Use `git restore tasks/TASKS.md` to bring back the deleted file.
    -   Delete all `tasks/{id}/task.json` files.
    -   Rename `tasks/{id}/plan.md` back to `tasks/{id}/plan_{id}.md`.
3.  **Disable New Tooling:** Comment out or revert the changes in `run_local_agent.py` that integrated the `task_utils.py` tooling.

The phased approach and the validation step (ensuring all tests pass) are designed to minimize the risk of needing a rollback.
