# Plan for Task 9: Automated tests

## Intent
Create automated tests for all currently existing tasks to verify their acceptance criteria, and ensure the project encodes the policy that a feature is only done once a test is written and passes. This plan will add tests for Tasks 1–8 and a meta-test for Task 9, aligning with docs/TESTING.md and docs/PLAN_SPECIFICATION.md.

## Context
- Specs: docs/TESTING.md, docs/PLAN_SPECIFICATION.md, docs/TASK_FORMAT.md
- Source files: tasks/TASKS.md, docs/*, scripts/run_local_agent.py

## Features

9.1) + Update spec
   Action: Update the `docs/PLAN_SPECIFICATION.md` file to include a section describing how testing works in this project. Include an example of what a test looks like, and explain how it verifies acceptance criteria.
   Acceptance:
   - The doc includes a section titled "Testing" which describes the process of writing tests for each task.
   - The section requires each task to have a folder named `tests`.
   - In the `tests` folder for a task, there is a test per each feature listed in the task's plan.
   - The feature tests are named according to the format `test_{task_id}_{feature_id}`, e.g. the test for this feature should be `test_9_1`.
   - There is an example test included as part of the description.
   - The plan doc should specify that the agent tries to complete a feature as a single step, gathers all the context required, and finishes by writing the tests for that feature.
   - When a feature is complete the agent sends back a `finish_feature` message that triggers the tool that commits all the current code and completes that feature.
   Context: docs/PLAN_SPECIFICATION.md
   Output: `docs/PLAN_SPECIFICATION.md`

9.2) - Create tests for Tasks 1–8
   Action: Write simple Python tests under tasks/{id}/tests/ to verify each task's acceptance criteria (primarily existence and key content of specified files).
   Acceptance:
   - For each of Tasks 1,2,3,4,5,6,7,8 there exists a test script at tasks/{id}/tests/ for each of the features that passes.
   - Tests check for expected files and key phrases tied to acceptance.
   - This task requires to gather context from whichever task is being looked at - if the `docs/PLAN_SPECIFICATION.md` is missing steps relating to this, it should be updated.
   Context: docs/TESTING.md, tasks/TASKS.md
   Output: `tasks/{task_id}/tests/test_{task_id}_{feature_id}.py` for all tasks up to this one and all their features
   Rejection: Not all features in a task have tests implemented. For instance `tasks/1/test_1_2.py` doesn't exist. The agent must inspect the context to see what's already there.

9.3) + Create a test runner script
   Action: Create a new script `scripts/run_tests.py`. It should run all tests found under `tasks/*/tests/*.py`.
   Acceptance:
   - Script runs successfully on local machine.
   Context: docs/TESTING.md
   Output: `scripts/run_tests.py`

9.4) - Create tests for this task
   Action: Add tests under this task verify docs/PLAN_SPECIFICATION.md encodes the test-driven policy (section "Test-Driven Acceptance").
   Acceptance:
   - Test checks presence of the section and the phrase that a feature is not complete until a corresponding test is written and passes.
   - All of the features here are tested by running `python scripts/run_tests.py`
   Context: docs/PLAN_SPECIFICATION.md, docs/TESTING.md
   Output: `tasks/{task_id}/tests/test_{task_id}_{feature_id}.py` for this task and all of its features
   Rejection: The test for this task doesn't check for the correct files or phrases. For instance `tasks/1/test_1_2.py` doesn't exist. The agent must inspect the context to see what's already there and create such a test that cleverly gathers the requirements and creates the test accordingly.

## Execution Steps
1) Implement features
2) Update `tasks/TASKS.md` with status change
3) Submit for review
4) Finish

---

## Manager Review — Clarifications and Constraints (Non-implementing)

The following refinements remove ambiguity and ensure testers and developers can proceed deterministically without additional guidance. No code is implemented by this change; it only clarifies the plan.

1) Scope and Sources for 9.2 (Tests for Tasks 1–8)
- Test Generation Basis: For each task in 1–8, enumerate its features exclusively from its plan file at `tasks/{id}/plan_{id}.md`.
- Per-Feature Tests: Create exactly one test file per feature, named `tasks/{id}/tests/test_{id}_{feature_number}.py`.
- Assertions: Each test must check the acceptance criteria of its corresponding feature. When acceptance depends on file existence or key phrases, assert those concrete conditions. When acceptance references a spec document, assert the presence of the referenced section/phrase in that document.
- Missing Plans/Specs: If a task lacks a plan file or acceptance criteria are undefined, mark the corresponding test effort as Unknown (`?`) in the plan (via feature status update) and use `ask_question` to request clarification. Do not fabricate acceptance criteria.

2) Test Discovery and Runner Conventions (Aligns with 9.3)
- Runner Entrypoint: `scripts/run_tests.py` is the single entry to run the entire suite.
- Discovery Pattern: The runner must discover tests under `tasks/*/tests/*.py`.
- Determinism: Tests must not depend on external network, API keys, or environment-specific state. Tests should operate solely on repository files.

3) Explicit Requirements for 9.4 (Meta-tests for this Task)
- Section Name: docs/PLAN_SPECIFICATION.md must include a section titled exactly "Test-Driven Acceptance".
- Mandatory Phrase: That section must contain the exact sentence: "A feature is not complete until a corresponding test is written and passes."
- Verification: The tests for 9.4 must assert both the presence of the section title and the exact sentence above.
- Execution: Verifying 9.4 is done by running `python scripts/run_tests.py` and seeing these tests pass.

4) Workflow and Status Tracking (Per docs/TOOL_ARCHITECTURE.md)
- Single Feature Focus: Implement and validate exactly one feature per agent cycle.
- Feature Completion Boundary: After implementing and validating a feature, call `finish_feature(task_id, feature_id, ...)` to create an isolated commit.
- Plan Status Updates: Update `tasks/{task_id}/plan_{task_id}.md` feature statuses as they progress (`-` Pending -> `~` In Progress -> `+` Completed). If ambiguity blocks progress, set `?` Unknown and use `ask_question`.
- Task Status in TASKS.md: When any feature of Task 9 is being actively worked on, set Task 9 status to `~` In Progress.

5) Non-Redundancy and References
- Do not restate implementation details in tests; reference docs/TESTING.md and docs/PLAN_SPECIFICATION.md for methodology and structure. Acceptance remains the authoritative source for "what"; specs define "how".

6) Current Status Summary for Task 9 (for visibility only)
- 9.1 Completed (+)
- 9.2 Pending (-)
- 9.3 Completed (+)
- 9.4 Pending (-)
