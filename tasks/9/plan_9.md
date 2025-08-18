# Plan for Task 9: Automated tests

## Intent
This plan will establish the principle of mandatory testing within the project's development workflow by updating the core planning specification. It will also lay out the features required to create tests for all previously completed tasks, ensuring the project adheres to this new standard retroactively.

## Context
- Specs: `docs/PLAN_SPECIFICATION.md`, `docs/TESTING.md`, `docs/FEATURE_FORMAT.md`
- Source files: `tasks/TASKS.md`

## Features
9.1) - Update Plan Specification to mandate testing
   Action: Modify `docs/PLAN_SPECIFICATION.md` to include a core principle that a feature is not considered complete until a corresponding test is written and passes. This formalizes the test-driven development approach for the agent.
   Acceptance:
   - `docs/PLAN_SPECIFICATION.md` contains a new section under "Core Principles" named "Test-Driven Acceptance".
   - This new section explicitly states that for every feature producing a tangible output, a subsequent feature must be created to write a test verifying its acceptance criteria.
   Context: `docs/PLAN_SPECIFICATION.md`, `docs/TESTING.md`
   Output: `docs/PLAN_SPECIFICATION.md`

9.2) - Create tests for Task 1 (Task format)
   Action: Create a test script to verify that `docs/TASK_FORMAT.md` was created correctly.
   Acceptance:
   - The file `tasks/1/tests/test_feature_1.py` exists.
   - The test script checks for the existence of `docs/TASK_FORMAT.md` and verifies it contains key sections.
   Context: `docs/TESTING.md`, `docs/TASK_FORMAT.md`
   Output: `tasks/1/tests/test_feature_1.py`

9.3) - Create tests for Task 2 (The spec)
   Action: Create a test script to verify that `docs/SPEC.md` was created correctly.
   Acceptance:
   - The file `tasks/2/tests/test_feature_1.py` exists.
   - The test script checks for the existence of `docs/SPEC.md`.
   Context: `docs/TESTING.md`, `docs/SPEC.md`
   Output: `tasks/2/tests/test_feature_1.py`

9.4) - Create tests for Task 3 (File organisation specification)
   Action: Create a test script to verify that `docs/FILE_ORGANISATION.md` was created correctly.
   Acceptance:
   - The file `tasks/3/tests/test_feature_1.py` exists.
   - The test script checks for the existence of `docs/FILE_ORGANISATION.md`.
   Context: `docs/TESTING.md`, `docs/FILE_ORGANISATION.md`
   Output: `tasks/3/tests/test_feature_1.py`

9.5) - Create tests for Task 4 (Specification documentation)
   Action: Create a test script to verify that `docs/SPECIFICATION_GUIDE.md` and `TEMPLATE.md` were created correctly.
   Acceptance:
   - The file `tasks/4/tests/test_feature_1.py` exists.
   - The test script checks for the existence of `docs/SPECIFICATION_GUIDE.md` and `docs/TEMPLATE.md`.
   Context: `docs/TESTING.md`, `docs/SPECIFICATION_GUIDE.md`
   Output: `tasks/4/tests/test_feature_1.py`

9.6) - Create tests for Task 5 (Plan specification)
   Action: Create a test script to verify that `docs/PLAN_SPECIFICATION.md` was created correctly.
   Acceptance:
   - The file `tasks/5/tests/test_feature_1.py` exists.
   - The test script checks for the existence of `docs/PLAN_SPECIFICATION.md`.
   Context: `docs/TESTING.md`, `docs/PLAN_SPECIFICATION.md`
   Output: `tasks/5/tests/test_feature_1.py`

9.7) - Create tests for Task 6 (Define Core Agent Terminology and Principles)
   Action: Create a test script to verify that `docs/AGENT_PRINCIPLES.md` was created correctly.
   Acceptance:
   - The file `tasks/6/tests/test_feature_1.py` exists.
   - The test script checks for the existence of `docs/AGENT_PRINCIPLES.md`.
   Context: `docs/TESTING.md`, `docs/AGENT_PRINCIPLES.md`
   Output: `tasks/6/tests/test_feature_1.py`

9.8) - Create tests for Task 7 (Agent Orchestrator)
   Action: Create a test script to verify that `scripts/run_local_agent.py` was created.
   Acceptance:
   - The file `tasks/7/tests/test_feature_1.py` exists.
   - The test script checks for the existence of `scripts/run_local_agent.py`.
   Context: `docs/TESTING.md`
   Output: `tasks/7/tests/test_feature_1.py`
   
9.9) - Create tests for Task 8 (Tests specification)
   Action: Create a test script to verify that `docs/TESTING.md` was created correctly.
   Acceptance:
   - The file `tasks/8/tests/test_feature_1.py` exists.
   - The test script checks for the existence of `docs/TESTING.md`.
   Context: `docs/TESTING.md`
   Output: `tasks/8/tests/test_feature_1.py`

## Execution Steps
1. Implement feature 9.1 by updating `docs/PLAN_SPECIFICATION.md`.
2. Update `tasks/TASKS.md` to mark Task 9 as 'In Progress'.
3. Submit for review.
4. Finish.
