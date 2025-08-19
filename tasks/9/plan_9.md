# Plan for Task 9: Automated tests

## Intent
Create automated tests for all currently existing tasks to verify their acceptance criteria, and ensure the project encodes the policy that a feature is only done once a test is written and passes. This plan will add tests for Tasks 1–8 and a meta-test for Task 9, aligning with docs/TESTING.md and docs/PLAN_SPECIFICATION.md.

## Context
- Specs: docs/TESTING.md, docs/PLAN_SPECIFICATION.md, docs/TASK_FORMAT.md
- Source files: tasks/TASKS.md, docs/*, scripts/run_local_agent.py

## Features
9.1) - Create acceptance tests for Tasks 1–8
   Action: Write simple Python tests under tasks/{id}/tests/ to verify each task's acceptance criteria (primarily existence and key content of specified files).
   Acceptance:
   - For each of Tasks 1,2,3,4,5,6,7,8 there exists a test script at tasks/{id}/tests/ that passes.
   - Tests check for expected files and key phrases tied to acceptance.
   Context: docs/TESTING.md, tasks/TASKS.md
   Output: tasks/1..8/tests/test_acceptance.py

9.2) - Meta-test for the testing policy
   Action: Add a test under Task 9 that verifies docs/PLAN_SPECIFICATION.md encodes the test-driven policy (section "Test-Driven Acceptance").
   Acceptance:
   - Test checks presence of the section and the phrase that a feature is not complete until a corresponding test is written and passes.
   Context: docs/PLAN_SPECIFICATION.md, docs/TESTING.md
   Output: tasks/9/tests/test_acceptance.py

9.3) - Verify per-task tests exist
   Action: The Task 9 meta-test verifies that for Tasks 1–8, a tests folder exists and contains at least one .py test file.
   Acceptance:
   - Meta-test passes confirming tests exist for Tasks 1–8.
   Context: docs/TESTING.md
   Output: tasks/9/tests/test_acceptance.py

## Execution Steps
1) Create test files for Tasks 1–8 per docs/TESTING.md.
2) Create Task 9 meta-test validating test policy and test presence.
3) Update tasks/TASKS.md to mark Task 9 as completed.
4) Submit for review.
5) Finish.
