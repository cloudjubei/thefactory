# Plan for Task 3: File organisation specification

## Intent
Create the File Organisation specification and its verifying test to satisfy Task 3's acceptance: a documented top-level directory layout, file naming conventions, and evolution guidance.

## Context
- Specs: docs/PLAN_SPECIFICATION.md, docs/FEATURE_FORMAT.md, docs/TASK_FORMAT.md
- Source files: tasks/TASKS.md

## Features
3.1) - Author File Organisation specification
   Action: Write docs/FILE_ORGANISATION.md describing the repository's structure and conventions.
   Acceptance:
   - docs/FILE_ORGANISATION.md exists
   - It includes clearly titled sections: "Top-Level Directory Layout", "File Naming Conventions", and "Evolution Guidance"
   - Each section provides concise explanations and examples where helpful
   Context: tasks/TASKS.md (Task 3), docs/TASK_FORMAT.md, docs/FEATURE_FORMAT.md, docs/PLAN_SPECIFICATION.md
   Output: docs/FILE_ORGANISATION.md

3.2) - Tests for File Organisation specification
   Action: Create a test that validates Feature 3.1's acceptance criteria.
   Acceptance:
   - tasks/3/tests/test_3_2.py exists
   - The test verifies that docs/FILE_ORGANISATION.md exists and contains the headings: "Top-Level Directory Layout", "File Naming Conventions", and "Evolution Guidance"
   - Running the test via run_tests passes
   Context: docs/PLAN_SPECIFICATION.md (Section 6: Testing)
   Dependencies: 3.1
   Output: tasks/3/tests/test_3_2.py

## Execution Steps
For each feature in order:
1) Gather context (MCC) using retrieve_context_files and implement the feature change
2) Create the test(s) that verify the feature's acceptance criteria under tasks/3/tests/
3) Run tests using the run_tests tool and ensure tests pass
4) Call finish_feature with a descriptive message (e.g., "Feature 3.{n} complete: {Title}") to create a commit for this feature

After all features are completed:
5) Run run_tests again and ensure the full suite passes
6) Update tasks/TASKS.md to mark Task 3 as completed
7) Submit for review (open PR)
8) Finish
