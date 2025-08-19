# Plan for Task 9: Automated tests

## Intent
Create automated tests for all currently existing tasks to verify their acceptance criteria, and ensure the project encodes the policy that a feature is only done once a test is written and passes. This plan will add tests for Tasks 1–8 and a meta-test for Task 9, aligning with docs/TESTING.md and docs/PLAN_SPECIFICATION.md.

## Context
- Specs: docs/TESTING.md, docs/PLAN_SPECIFICATION.md, docs/TASK_FORMAT.md
- Source files: tasks/TASKS.md, docs/*, scripts/run_local_agent.py

## Features
9.1) - Create tests for Tasks 1–8
   Action: Write simple Python tests under tasks/{id}/tests/ to verify each task's acceptance criteria (primarily existence and key content of specified files).
   Acceptance:
   - For each of Tasks 1,2,3,4,5,6,7,8 there exists a test script at tasks/{id}/tests/ for each of the features that passes.
   - Tests check for expected files and key phrases tied to acceptance.
   Context: docs/TESTING.md, tasks/TASKS.md
   Output: `tasks/{task_id}/tests/test_{task_id}_{feature_id}.py` for all tasks up to this one and all their features

9.2) - Create a test runner script
   Action: Create a new script `scripts/run_tests.py`. It should run all tests found under `tasks/*/tests/*.py`.
   Acceptance:
   - Script runs successfully on local machine.
   Context: docs/TESTING.md
   Output: `scripts/run_tests.py`

9.3) - Create tests for this task
   Action: Add tests under this task verify docs/PLAN_SPECIFICATION.md encodes the test-driven policy (section "Test-Driven Acceptance").
   Acceptance:
   - Test checks presence of the section and the phrase that a feature is not complete until a corresponding test is written and passes.
   - All of the features here are tested by running `python scripts/run_tests.py`
   Context: docs/PLAN_SPECIFICATION.md, docs/TESTING.md
   Output: `tasks/{task_id}/tests/test_{task_id}_{feature_id}.py` for this task and all of its features

## Execution Steps
1) Implement features
2) Update `tasks/TASKS.md` with status change
3) Submit for review
4) Finish
