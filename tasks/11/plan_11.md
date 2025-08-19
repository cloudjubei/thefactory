# Plan for Task 11: JSON-based tasks format migration specification

## Intent
Define the canonical JSON-based per-task format and a migration guide from tasks/TASKS.md to tasks/{id}/task.json, and update the Task Format to reference this JSON format and the compatibility period. Ensure implementation follow-up tasks (25–28) are listed as pending.

## Context
- Specs: docs/PLAN_SPECIFICATION.md, docs/FEATURE_FORMAT.md, docs/TASK_FORMAT.md, docs/TESTING.md, docs/TOOL_ARCHITECTURE.md
- Source files: tasks/TASKS.md

## Features
11.1) + Author the JSON-based tasks format specification (TASKS_JSON_FORMAT.md)
   Action: Create a single-entry specification describing the per-task folder layout and task.json schema, including features structure and metadata, reusing status code definitions from docs/TASK_FORMAT.md.
   Acceptance:
   - docs/TASKS_JSON_FORMAT.md exists.
   - Defines folder structure: tasks/{id}/ containing task.json, plan_{id}.md, tests/, optional artifacts/.
   - Defines task.json fields: id, status, title, action, acceptance (array[string] or structured), notes (optional), dependencies (optional), features (array of objects with: number, status, title, action, acceptance, context, dependencies, output, notes), metadata (created, updated, version).
   - References status code definitions from docs/TASK_FORMAT.md.
   - Includes end-to-end examples for a task and one feature.
   Context: docs/TASK_FORMAT.md, docs/FEATURE_FORMAT.md
   Output: docs/TASKS_JSON_FORMAT.md
   Notes: Canonical source of truth for tasks after migration.

11.2) + Author the migration guide (TASKS_MIGRATION_GUIDE.md)
   Action: Provide a stepwise migration plan with dual-read compatibility, orchestrator/context selection requirements, test/CI impacts, rollback plan, and deprecation strategy.
   Acceptance:
   - docs/TASKS_MIGRATION_GUIDE.md exists.
   - Includes dual-read compatibility plan between TASKS.md and task.json.
   - Details persona-scoped context requirements for orchestrator updates.
   - References docs/TESTING.md and describes schema validation in CI.
   - Documents rollback plan and deprecation strategy for TASKS.md.
   Context: docs/TESTING.md, docs/PLAN_SPECIFICATION.md, scripts/run_local_agent.py
   Output: docs/TASKS_MIGRATION_GUIDE.md

11.3) + Update Task Format to reference JSON canonical format and compatibility section
   Action: Update docs/TASK_FORMAT.md to:
   - Reference docs/TASKS_JSON_FORMAT.md as the canonical source of truth for tasks.
   - Add a compatibility section for tasks/TASKS.md until migration completes.
   Acceptance:
   - docs/TASK_FORMAT.md updated with clear canonical reference to JSON format.
   - Compatibility/migration notes link to docs/TASKS_MIGRATION_GUIDE.md.
   Context: docs/TASKS_JSON_FORMAT.md, docs/TASKS_MIGRATION_GUIDE.md
   Output: Updated docs/TASK_FORMAT.md

11.4) + Ensure implementation tasks are listed as pending
   Action: Confirm that tasks 25–28 exist in tasks/TASKS.md as pending, aligned with the migration plan.
   Acceptance:
   - tasks 25, 26, 27, 28 are present and pending with correct titles matching the migration steps.
   - No additional changes required if already present.
   Context: tasks/TASKS.md, docs/TASKS_MIGRATION_GUIDE.md
   Output: Verified task list (no new files)
   Notes: Already present at the time of this plan.

## Execution Steps
For this documentation-only task, implement all features in one atomic cycle:
1) Write docs/TASKS_JSON_FORMAT.md and docs/TASKS_MIGRATION_GUIDE.md.
2) Update docs/TASK_FORMAT.md to reference JSON canonical format and add compatibility guidance.
3) Verify tasks 25–28 exist (they do) and update tasks/TASKS.md to mark Task 11 as completed (+).
4) Submit for review and finish.
