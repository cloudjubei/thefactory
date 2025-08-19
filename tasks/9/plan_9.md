# Plan for Task 9: Automated tests

## Intent
Create automated tests for all currently existing tasks to verify their acceptance criteria, and ensure the project encodes the policy that a feature is only done once a test is written and passes. This plan adds/maintains tests for Tasks 1–8 and meta-tests for Task 9, aligning with project specifications.

## Context
- Specs: docs/PLAN_SPECIFICATION.md, docs/FEATURE_FORMAT.md, docs/TASK_FORMAT.md, docs/TOOL_ARCHITECTURE.md, docs/TESTING.md
- Source files: tasks/TASKS.md, scripts/run_local_agent.py

## Features

9.1) - Update spec
   Action: Update the `docs/PLAN_SPECIFICATION.md` file to include a section describing how testing works in this project. Include an example of what a test looks like, and explain how it verifies acceptance criteria.
   Acceptance:
   - The doc includes a section titled "Testing" which describes the process of writing tests for each task.
   - The section requires each task to have a folder named `tests`.
   - In the `tests` folder for a task, there is a test per each feature listed in the task's plan.
   - The feature tests are named according to the format `test_{task_id}_{feature_id}`, e.g. the test for this feature should be `test_9_1`.
   - There is an example test included as part of the description.
   - The plan doc specifies per-feature single-step delivery: the agent gathers context, implements, writes tests, runs tests, and calls `finish_feature`.
   - When a feature is complete the agent sends back a `finish_feature` message that triggers the commit for that feature.
   Context: docs/PLAN_SPECIFICATION.md
   Dependencies: None
   Output: docs/PLAN_SPECIFICATION.md
   Notes: Completed in prior work; retained here for traceability.

9.2) - Create tests for Tasks 1–8
   Action: Write simple Python tests under `tasks/{id}/tests/` to verify each task's acceptance criteria (primarily existence and key content of specified files). Ensure one test per feature in each task's plan.
   Acceptance:
   - For each of Tasks 1,2,3,4,5,6,7,8 there exists a test script at `tasks/{id}/tests/` for each of the features that passes.
   - Tests check for expected files and key phrases tied to acceptance.
   - This task requires gathering context from each target task; if `docs/PLAN_SPECIFICATION.md` is missing steps relating to this, it should be updated.
   Context: docs/TESTING.md, tasks/TASKS.md, docs/PLAN_SPECIFICATION.md
   Dependencies: 9.3 (test runner available)
   Output: `tasks/{task_id}/tests/test_{task_id}_{feature_id}.py` for all tasks up to this one and all their features
   Notes: Ensure naming strictly follows `test_{task_id}_{feature_id}.py`.
   Rejection: Not all features in a task have tests implemented (e.g., missing `tasks/1/tests/test_1_2.py`).

9.3) + Create a test runner script
   Action: Create a script `scripts/run_tests.py`. It should discover and run all tests under `tasks/*/tests/*.py` and provide a summary.
   Acceptance:
   - Script runs successfully on a local machine.
   - Returns an exit code 0 on success and non-zero on failure.
   Context: docs/TESTING.md
   Dependencies: None
   Output: scripts/run_tests.py
   Notes: Completed in prior work; retained here for traceability.

9.4) + Create tests for this task
   Action: Add tests under this task that verify docs/PLAN_SPECIFICATION.md encodes the test-driven policy (section "Test-Driven Acceptance").
   Acceptance:
   - Test checks presence of the section and the phrase that a feature is not complete until a corresponding test is written and passes.
   - All of the features here are tested by running `python scripts/run_tests.py`.
   Context: docs/PLAN_SPECIFICATION.md, docs/TESTING.md
   Dependencies: 9.1, 9.3
   Output: `tasks/9/tests/test_9_4.py` (and tests validating other features in this task)
   Notes: Ensure the test locates and checks the exact phrases specified in the spec.
   Rejection: The test for this task doesn't check for the correct files or phrases.

## Execution Steps
For each feature in order:
1) Gather context (Minimum Cohesive Context) using `retrieve_context_files` for: tasks/TASKS.md; this plan file; all referenced specs (docs/PLAN_SPECIFICATION.md, docs/FEATURE_FORMAT.md, docs/TASK_FORMAT.md, docs/TOOL_ARCHITECTURE.md, docs/TESTING.md); and any files to be created/modified.
2) Implement the feature changes using `write_file` (create or update the required files under docs/ or tasks/{id}/tests/ as specified).
3) Create the test(s) that verify the feature's acceptance criteria under `tasks/{task_id}/tests/`, named `test_{task_id}_{feature_id}.py`.
4) Run tests using the `run_tests` tool and ensure tests pass. Then call `finish_feature` with a descriptive message (e.g., "Feature 9.{n} complete: {Title}") to create a commit for this feature.

After all features are completed:
5) Run `run_tests` again and ensure the full suite passes.
6) Update `tasks/TASKS.md` marking Task 9 as completed (+) once all features are completed and passing.
7) Call `submit_for_review` for Task 9.
8) Call `finish` to end the cycle.
