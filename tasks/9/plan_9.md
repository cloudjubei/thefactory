# Plan for Task 9: Refactor Task and Feature Format

## Intent
This plan outlines the steps to refactor the project's task and feature management system. The current markdown-based approach in `tasks/TASKS.md` and per-task plans will be replaced with a structured, per-task `task.json` file. This change is motivated by the need to provide more precise and minimal context to different AI agent personas, thereby improving their efficiency and accuracy. This plan focuses on updating the specifications and planning for the necessary tooling and migration, preparing the groundwork for implementation.

## Context
- Specs: `docs/TASK_FORMAT.md`, `docs/PLAN_SPECIFICATION.md`, `docs/FEATURE_FORMAT.md`, `docs/TOOL_ARCHITECTURE.md`
- Source files: `tasks/TASKS.md`, `scripts/run_local_agent.py`

## Features
9.1) - Define `task.json` schema in TASK_FORMAT.md
   Action: Update the task format specification to define a new, canonical JSON structure for tasks. This moves the single source of truth for a task's definition from markdown files into a structured `task.json` file.
   Acceptance:
     - `docs/TASK_FORMAT.md` is updated to describe the `tasks/{task_id}/task.json` file as the primary source for task data.
     - The document includes a clear JSON schema for `task.json`, detailing all required fields (id, title, status, action, acceptance, notes, dependencies) and a `features` array.
     - The schema for items in the `features` array must conform to `docs/FEATURE_FORMAT.md`.

9.2) - Adapt PLAN_SPECIFICATION.md to the new format
   Action: Modify the plan specification to align with features being defined in `task.json`. The plan file will now serve as a high-level strategic document for the agent's execution approach, rather than the container for feature definitions.
   Acceptance:
     - `docs/PLAN_SPECIFICATION.md` is updated to remove the enumeration of features from its template.
     - The document clarifies that the plan is a strategic guide, while `task.json` is the canonical source for feature details.
     - Examples within the specification are updated to reflect this new separation of concerns.

9.3) - Specify new data access tools in TOOL_ARCHITECTURE.md
   Action: Document the design of new tools required to interact with the `task.json` files. This provides the specification for developers to implement the necessary low-level data access.
   Acceptance:
     - `docs/TOOL_ARCHITECTURE.md` is updated with specifications for new tools.
     - A `read_task(task_id)` tool is defined, which returns the full JSON content of a task.
     - A `write_task(task_id, task_data)` tool is defined, which overwrites a task's JSON file.
     - A `list_tasks()` tool is defined to list all available tasks by scanning the `tasks/` directory.
     - Existing tools that read from `plan.md` (e.g., `read_plan_feature`) are marked for deprecation or update.

9.4) - Plan the migration of existing tasks
   Action: Define the requirements for a one-off script to migrate all existing tasks from the markdown format to the new `task.json` structure.
   Acceptance:
     - A new feature is added to this plan (e.g., as 9.7 or similar, to be implemented by a developer) for the creation of `scripts/migrate_tasks_to_json.py`.
     - The acceptance criteria for the migration script feature specifies that it must parse `tasks/TASKS.md` and all `tasks/{task_id}/plan_{task_id}.md` files to generate valid `task.json` files.

9.5) - Plan updates to the agent orchestrator
   Action: Define the requirements for updating the agent orchestrator to work with the new `task.json` structure.
   Acceptance:
     - A new feature is added to this plan for the modification of `scripts/run_local_agent.py`.
     - The acceptance criteria for this feature specifies that the `_gather_context` method must be updated to identify and load tasks from `task.json` files.

9.6) - Redefine the purpose of tasks/TASKS.md
   Action: After migration, the central `tasks/TASKS.md` file will be obsolete for holding task details. This feature plans for its simplification.
   Acceptance:
     - A new feature is added to this plan to simplify `tasks/TASKS.md`.
     - The acceptance criteria for this feature states that `tasks/TASKS.md` should be converted into a simple index, listing only the task ID and title, and pointing to the task's directory.

## Execution Steps
1. Create this plan file `tasks/9/plan_9.md`.
2. Update `tasks/TASKS.md` to change the status of Task 9 from `?` to `-` to indicate it is now planned and pending implementation.
3. Submit for review.

## Administrative Steps
- Update `tasks/TASKS.md`
- `submit_for_review`
- `finish`
