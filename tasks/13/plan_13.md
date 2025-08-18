# Plan for Task 13: Tasks, Plans and Features

## Intent
Introduce a formal features format, mandate per-task plans, and align repository documentation so that every task is executed via a plan at tasks/{id}/plan_{id}.md with an enumerated feature list.

## Context
- docs/SPEC.md
- docs/TASK_FORMAT.md
- docs/PLAN_SPECIFICATION.md
- docs/FEATURE_FORMAT.md (to be created)
- docs/FILE_ORGANISATION.md
- tasks/TASKS.md

## Features
13.1) Create Feature Format specification
   Action: Provide a dedicated specification for features to ensure consistent structure across plans.
   Acceptance:
   - docs/FEATURE_FORMAT.md exists and includes Purpose, Where Features Live, Numbering, Format, Success Criteria, Example, and Checklist
   Context: docs/SPECIFICATION_GUIDE.md, docs/TASK_FORMAT.md
   Dependencies: None
   Output: docs/FEATURE_FORMAT.md

13.2) Update Task Format with plan/feature workflow
   Action: Update docs/TASK_FORMAT.md to require creating a per-task plan and to reference FEATURE_FORMAT.md.
   Acceptance:
   - docs/TASK_FORMAT.md contains sections "Plans and Features Workflow" and "Agent Execution Path"
   - It mandates `tasks/{task_id}/plan_{task_id}.md` and references `docs/FEATURE_FORMAT.md`
   Context: docs/TASK_FORMAT.md, docs/FEATURE_FORMAT.md
   Dependencies: 13.1
   Output: Updated docs/TASK_FORMAT.md

13.3) Update Plan Specification to include features and location
   Action: Ensure docs/PLAN_SPECIFICATION.md defines plan location, required sections, and a template with a Features section referencing FEATURE_FORMAT.md.
   Acceptance:
   - docs/PLAN_SPECIFICATION.md states the location `tasks/{task_id}/plan_{task_id}.md`
   - Includes a plan template with a Features section
   Context: docs/PLAN_SPECIFICATION.md, docs/FEATURE_FORMAT.md
   Dependencies: 13.1
   Output: Updated docs/PLAN_SPECIFICATION.md

13.4) Update SPEC actions to include plan creation
   Action: Update docs/SPEC.md ACTIONS to require reading PLAN_SPECIFICATION.md and creating a per-task plan with features before implementing.
   Acceptance:
   - docs/SPEC.md ACTIONS list includes reading PLAN_SPECIFICATION.md and creating `tasks/{id}/plan_{id}.md`
   Context: docs/SPEC.md, docs/PLAN_SPECIFICATION.md
   Dependencies: 13.2, 13.3
   Output: Updated docs/SPEC.md

13.5) Update File Organisation to reflect per-task plans
   Action: Update docs/FILE_ORGANISATION.md to document plans under tasks/{id}/ and deprecate any separate top-level plans directory.
   Acceptance:
   - docs/FILE_ORGANISATION.md shows tasks/{id}/plan_{id}.md in the structure
   - Notes that a top-level plans/ directory is deprecated
   Context: docs/FILE_ORGANISATION.md
   Dependencies: 13.2, 13.3
   Output: Updated docs/FILE_ORGANISATION.md

13.6) Mark Task 13 completed
   Action: Update tasks/TASKS.md to set Task 13 status to '+' Completed.
   Acceptance:
   - tasks/TASKS.md lists Task 13 with status '+'
   Context: tasks/TASKS.md
   Dependencies: 13.1–13.5
   Output: Updated tasks/TASKS.md

## Execution Steps
1) Create docs/FEATURE_FORMAT.md (13.1)
2) Update docs/TASK_FORMAT.md (13.2)
3) Update docs/PLAN_SPECIFICATION.md (13.3)
4) Update docs/SPEC.md (13.4)
5) Update docs/FILE_ORGANISATION.md (13.5)
6) Update tasks/TASKS.md: mark Task 13 as completed (13.6)
7) Submit for review and finish
