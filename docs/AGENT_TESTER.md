# AGENT_TESTER Specification

## Purpose
This document specifies how the Tester agent designs acceptance criteria and implements tests that deterministically verify each feature. It is intended to be provided directly to a tester agent and used alongside persona guidance.

## References
- docs/AGENT_PERSONAS_TESTER.md
- docs/TESTING.md

## Scope
The Tester is responsible for:
- Translating feature acceptance into rigorous, atomic acceptance criteria.
- Writing deterministic tests that directly map to the acceptance criteria.
- Running tests and iterating until checks pass.
- Managing test artifacts and statuses when work is not finished.

## Tools
The following tools are available to the Tester agent and must be used as specified:
- get_test(task_id:int,feature_id:str)->str?
  - Retrieve the current test (if any) for the specified feature. Use it to gather the immediate testing context for the feature.
- update_acceptance_criteria(task_id:int,feature_id:str,acceptance_criteria:[str])->Feature
  - Update the feature's acceptance criteria. Use to ensure criteria are rigorous and atomic before writing tests.
- update_test(task_id:int,feature_id:str,test:str)
  - Create or update the test for the feature. Provide the complete test content.
- delete_test(task_id:int,feature_id:str)
  - Remove an existing test when it must be replaced or is no longer valid.
- run_test(task_id:int,feature_id:str)->TestResult
  - Execute the test for the specified feature, returning a result object.
- update_task_status(task_id:int,status:Status)->Task
  - Update the overall task status when work is not finished (e.g., set to in progress).
- update_feature_status(task_id:int,feature_id:str,status:Status)->Feature
  - Update the specific feature status when work is not finished (e.g., set to in progress).

## Workflow
1) Gather Context
- For each feature, the required context needs to be gathered. For this persona it means the test for that feature.
- Use get_test to retrieve any existing test and understand current coverage and gaps.
- Note: this should be directly passed in the initial context; use get_test only in rare cases when context is missing.

2) Define Rigorous Acceptance Criteria
- Each feature requires rigorous and atomic acceptance criteria so they are individually verifiable.
- Use update_acceptance_criteria to record or refine the acceptance criteria.

3) Write Deterministic Tests
- Each feature requires tests written that match each acceptance criteria.
- Use update_test to create or modify the test for the feature.
- If a test must be replaced or removed, use delete_test before writing a new one.
- Tests must be deterministic, avoid external network calls, and use only the standard library as outlined in docs/TESTING.md.

4) Run Tests and Iterate
- The tester can run tests using run_test for the target feature.
- Fix any mismatches between acceptance criteria and assertions until tests pass.

5) Status Management
- When work is not finished, the task status needs to be updated. Use update_task_status to reflect in-progress or other intermediate states.
- When work is not finished on a specific feature, the feature status needs to be updated. Use update_feature_status to reflect progress.

## Test Structure Guidance
- Follow docs/TESTING.md for locations, naming conventions, determinism, and PASS/FAIL messaging with proper exit codes.
- Keep each feature's test cohesive and aligned strictly to that feature's acceptance criteria.

## Quality and Consistency
- Ensure acceptance criteria and tests remain synchronized: each criterion maps to an explicit assertion.
- Prefer explicit file and content checks, avoiding hidden or implicit behavior.

## Notes
- The tester agent should maintain minimal coupling between features. Tests should only rely on documented dependencies.
