# Plan for Task 11: The plans for all tasks must be updated

## Intent
Backfill and/or update per-task plans so that tasks 1–10 each have a standards-compliant plan that reflects current status and acceptance, while clarifying legacy handling for pre-existing completed tasks. Ensure PLAN_SPECIFICATION clarifies how to treat legacy tasks and backfilled test features without retroactively changing historical task statuses.

## Context
- Specs: docs/SPEC.md, docs/TASK_FORMAT.md, docs/PLAN_SPECIFICATION.md, docs/FEATURE_FORMAT.md, docs/TESTING.md
- Source files: tasks/TASKS.md

## Features
11.1) - Update PLAN_SPECIFICATION with Legacy/Backfill guidance
   Action: Add a section to docs/PLAN_SPECIFICATION.md detailing how to handle already-completed (legacy) tasks when backfilling plans and test-writing features, including not retroactively changing TASKS.md statuses unless acceptance criteria are actually missing.
   Acceptance:
   - docs/PLAN_SPECIFICATION.md includes a section titled "Legacy Tasks and Backfilled Plans" (or similar) with clear rules
   - Rules state that test-writing features for legacy tasks may be marked Blocked (dependency on Task 9) and do not force changing Completed task statuses in tasks/TASKS.md
   - The section references the rationale and MCC usage
   Context: docs/PLAN_SPECIFICATION.md, docs/FEATURE_FORMAT.md
   Output: Updated docs/PLAN_SPECIFICATION.md

11.2) - Backfill plans for tasks 1–10
   Action: Create tasks/{id}/plan_{id}.md for tasks 1 through 10 that follow PLAN_SPECIFICATION. Enumerate features that map to the task's output(s). For legacy tasks already marked Completed, include a Blocked test-writing feature with dependency on Task 9. Pending tasks remain Pending with appropriately defined features.
   Acceptance:
   - The files tasks/1/plan_1.md through tasks/10/plan_10.md exist
   - Each plan includes Title, Intent, Context, Features, and Execution Steps as per PLAN_SPECIFICATION
   - For tasks 1,2,3,4,5,6,7,8, features reflect delivered docs/scripts as Completed and include a Blocked test-writing feature (dependency on Task 9)
   - For task 4, include a Pending feature to create TEMPLATE.md per the task's notes
   - For task 9, enumerate Pending features for the automated tests effort
   - For task 10, enumerate Pending features for merging tasks 6 & 7
   Output: tasks/{id}/plan_{id}.md for ids 1–10
   Dependencies: 11.1

## Execution Steps
For each feature in order:
1) Gather MCC using retrieve_context_files
2) Implement changes with write_file
3) Create tests under tasks/11/tests/ to verify acceptance
4) Run tests using run_tests and ensure they pass
5) Call finish_feature for the completed feature

After all features are completed:
6) Update tasks/TASKS.md to mark task 11 as completed
7) Submit for review
8) Finish
