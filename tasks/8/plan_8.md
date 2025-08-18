# Plan for Task 8: Cleanup

## Intent
Ensure all files and tasks follow current specifications, correct inconsistencies, backfill missing plan files, and align documentation paths with file organisation conventions.

## Context
- Specs: docs/SPEC.md, docs/TASK_FORMAT.md, docs/FILE_ORGANISATION.md, docs/FEATURE_FORMAT.md, docs/PLAN_SPECIFICATION.md, docs/AGENT_PRINCIPLES.md
- Files: tasks/TASKS.md, existing docs/*, tasks/*

## Features
8.1) Backfill per-task plan files
   Action: Create tasks/{id}/plan_{id}.md for tasks 1–9 to comply with Plan Specification.
   Acceptance: Plan files exist for tasks 1–9 using docs/FEATURE_FORMAT.md.
   Output: tasks/1/plan_1.md ... tasks/9/plan_9.md

8.2) Correct task statuses
   Action: Audit task acceptances vs artifacts; update statuses accordingly (e.g., mark Task 7 as Pending until implemented).
   Acceptance: tasks/TASKS.md accurately reflects reality.
   Output: Updated tasks/TASKS.md

8.3) Add TEMPLATE.md
   Action: Create docs/TEMPLATE.md per Task 4 notes with section placeholders and examples from the guide.
   Acceptance: docs/TEMPLATE.md exists.
   Output: docs/TEMPLATE.md

8.4) Align documentation paths
   Action: Normalize acceptance criteria for pending/unknown tasks to use docs/ paths per FILE_ORGANISATION.md.
   Acceptance: Tasks 17–21 reference docs/ paths for documentation files.
   Output: Updated tasks/TASKS.md

## Execution Steps
1) Create plan files for tasks 1–9
2) Create docs/TEMPLATE.md
3) Update tasks/TASKS.md: fix statuses, normalize doc paths, mark Task 8 complete
4) Submit for review
5) Finish
