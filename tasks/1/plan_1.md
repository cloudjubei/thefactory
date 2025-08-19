# Plan for Task 1: Task format

## Intent
Document the canonical task format to ensure consistency and testability across the project.

## Context
- Specs: docs/SPEC.md, docs/TASK_FORMAT.md, docs/PLAN_SPECIFICATION.md, docs/FEATURE_FORMAT.md, docs/TESTING.md
- Source files: tasks/TASKS.md

## Features
1.1) + Create the Task Format specification
   Action: Author docs/TASK_FORMAT.md defining the fields, statuses, rules, and examples for tasks.
   Acceptance:
   - docs/TASK_FORMAT.md exists and describes ID, Status, Action, Acceptance, Notes
   - Includes Rules and Tips and examples
   Context: docs/SPECIFICATION_GUIDE.md, docs/FEATURE_FORMAT.md
   Output: docs/TASK_FORMAT.md

1.2) / Write tests for the Task Format specification
   Action: Create a test under tasks/1/tests/ that verifies docs/TASK_FORMAT.md exists and contains required sections.
   Acceptance:
   - tests under tasks/1/tests/ verify presence and sections
   Dependencies: 9.1
   Notes: Legacy task; tests to be implemented under Task 9.

## Execution Steps
- Backfilled: No further action required for 1.1 (already completed).
- Tests for 1.2 will be added by Task 9; no status change needed for Task 1.
