# Plan for Task 13: JSON-based tasks format

## Intent
This plan outlines the features required to transition from the current Markdown-based task management system (`tasks/TASKS.md`) to a structured, JSON-based format. The transition will be phased to ensure stability, starting with schema definition, followed by tooling, migration, and finally, cleanup. This will make task management more robust, machine-readable, and extensible.

## Context
- Specs: docs/SPEC.md, docs/tasks/TASKS_GUIDANCE.md, docs/PLAN_SPECIFICATION.md, docs/FEATURE_FORMAT.md, docs/TESTING.md
- Source files: tasks/13/task.json, scripts/run_local_agent.py

## Features

### Phase 1: Specification & Definition
13.1) + Define Task Schema in Python
   Action: Create `docs/tasks/task_format.py` to define the new task structure using Python's `TypedDict` or similar data classes. This will serve as the canonical schema for tasks, features, and related objects.
   Acceptance:
     - `docs/tasks/task_format.py` exists.
     - The file defines Python types for `Task`, `Feature`, and other relevant data structures.
     - The types cover all fields currently used in `TASKS.md` and `plan.md` files.
   Output: `docs/tasks/task_format.py`

13.2) + Create Example JSON Task File
   Action: Create `docs/tasks/task_example.json` that demonstrates a complete task in the new format, adhering to the schema defined in `task_format.py`.
   Acceptance:
     - `docs/tasks/task_example.json` exists.
     - The JSON is valid and conforms to the structure defined in `docs/tasks/task_format.py`.
   Dependencies: 13.1
   Output: `docs/tasks/task_example.json`

13.3) + Write Migration Guide
   Action: Create `docs/tasks/TASKS_MIGRATION_GUIDE.md` detailing the step-by-step plan to migrate from the old format to the new one.
   Acceptance:
     - `docs/tasks/TASKS_MIGRATION_GUIDE.md` exists.
     - The guide includes a migration plan, backward compatibility strategy, tooling requirements, and a rollback plan.
   Output: `docs/tasks/TASKS_MIGRATION_GUIDE.md`

13.4) + Update Task Authoring Guidance
   Action: Move `docs/TASK_FORMAT.md` to `docs/tasks/TASKS_GUIDANCE.md` and update its content to align with the new JSON format, removing schema definitions now covered by `task_format.py` and focusing on authoring best practices.
   Acceptance:
     - `docs/TASK_FORMAT.md` is removed.
     - `docs/tasks/TASKS_GUIDANCE.md` exists.
     - The content of the new guidance file is updated to reflect the JSON-based workflow.
   Dependencies: 13.1
   Output: `docs/tasks/TASKS_GUIDANCE.md`

### Phase 2: Tooling & Integration
13.5) + Create Task Utility Tooling
   Action: Create a new tool module `scripts/tools/task_utils.py` with functions to reliably read, create, and update tasks in the new JSON format. This will abstract file I/O for task manipulation.
   Acceptance:
     - `scripts/tools/task_utils.py` exists.
     - It contains functions like `get_task(task_id)`, `update_task(task_id, task_data)`, `create_task(...)`.
     - Functions are well-documented and include error handling.
   Dependencies: 13.1
   Output: `scripts/tools/task_utils.py`

13.6) + Integrate Tooling into Orchestrator with Dual-Read Mode
   Action: Update the orchestrator (`run_local_agent.py`) to use `task_utils.py` for task operations. Implement a dual-read mode that can read from both `tasks/{id}/task.json` and the old `tasks/TASKS.md` during the transition period.
   Acceptance:
     - `run_local_agent.py` is updated to import and use `task_utils.py`.
     - The orchestrator can correctly parse task information from both the old Markdown file and the new JSON file structure.
   Dependencies: 13.5
   Output: Modified `scripts/run_local_agent.py`

### Phase 3: Migration & Validation
13.7) + Implement Migration Script
   Action: Create a script `scripts/migrate_tasks.py` that reads all tasks from `tasks/TASKS.md` and their corresponding plans and tests, and converts them to the new directory structure (`tasks/{id}/task.json`, `tasks/{id}/plan.md`, etc.).
   Acceptance:
     - `scripts/migrate_tasks.py` exists.
     - The script can be run to perform the full migration of all existing tasks.
     - The script correctly handles task descriptions, features from plans, and relocates test files.
   Dependencies: 13.5
   Output: `scripts/migrate_tasks.py`

13.8) - Execute Migration, Embed Plans, and Validate
   Action: Run the migration script to convert all existing tasks. The script must embed the content of `plan.md` files into the `plan` field of the corresponding `task.json` task and feature objects, and then delete the source `plan.md` files.
   Acceptance:
     - All tasks from `TASKS.md` now exist in the `tasks/{id}/task.json` format.
     - The `plan` field in each `task.json` and its features contains the content from the original `plan.md`.
     - All associated `plan.md` files are removed from their new locations (`tasks/{id}/`).
     - All project tests pass after the migration using `run_tests`.
   Dependencies: 13.7

### Phase 4: Cleanup
13.9) - Remove Dual-Read Mode from Orchestrator
   Action: Remove the backward-compatibility code (dual-read mode) from `run_local_agent.py`, making the JSON format the sole source of truth for tasks.
   Acceptance:
     - The orchestrator (`run_local_agent.py`) is simplified to only read from `tasks/{id}/task.json` using `task_utils.py`.
     - The agent continues to function correctly.
   Dependencies: 13.8
   Output: Modified `scripts/run_local_agent.py`

13.10) - Remove TASKS.md
   Action: Delete the old `tasks/TASKS.md` file from the repository to complete the migration.
   Acceptance:
     - `tasks/TASKS.md` is deleted.
   Dependencies: 13.9

13.11) - Update Guidance and Tooling for Plan-in-JSON
   Action: Update documentation and scripts to align with the plan-in-JSON format. This includes updating `PLAN_SPECIFICATION.md` and `FILE_ORGANISATION.md`. Also, update the `_gather_context` function in `run_local_agent.py` and add a new helper function to `task_utils.py` for updating feature status directly in the `task.json` file.
   Acceptance:
     - `docs/PLAN_SPECIFICATION.md` is updated to describe the `plan` field in `task.json`.
     - `docs/FILE_ORGANISATION.md` is updated to reflect that `plan.md` is deprecated.
     - A new function, e.g., `update_feature_status(task_id, feature_id, new_status)`, exists in `scripts/tools/task_utils.py`.
     - `scripts/run_local_agent.py`'s `_gather_context` function is updated to read `task.json` instead of `plan.md`.
   Dependencies: 13.8

13.12) - Remove Migration Guide
   Action: Remove `docs/tasks/TASKS_MIGRATION_GUIDE.md` and any references to it, as the migration is complete.
   Acceptance:
     - `docs/tasks/TASKS_MIGRATION_GUIDE.md` is removed.
   Dependencies: 13.10, 13.11

13.13) - Final Cleanup
   Action: This task definition file (`tasks/13/task.json`) will be removed as the final step of its own completion, closing the loop on the migration.
   Acceptance:
     - `tasks/13/task.json` is removed.
   Dependencies: 13.12

## Execution Steps
For each feature in order:
1) Gather context (MCC) using `retrieve_context_files` and implement the feature changes
2) Create the test(s) that verify the feature's acceptance criteria under `tasks/13/tests/`
3) Run tests using the `run_tests` tool and ensure tests pass
4) Call `finish_feature` with a descriptive message (e.g., "Feature 13.1 complete: Define Task Schema in Python") to create a commit for this feature

After all features are completed:
5) Run `run_tests` again and ensure the full suite passes
6) Submit for review (open PR)
7) Finish
