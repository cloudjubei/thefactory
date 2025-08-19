# Plan for Task 8: Tests specification

## Intent
Establish the canonical, project-wide testing specification and integrate testing requirements into the planning specification so every feature is verifiable by deterministic tests.

## Context
- Specs: docs/TASK_FORMAT.md, docs/PLAN_SPECIFICATION.md, docs/FEATURE_FORMAT.md, docs/TOOL_ARCHITECTURE.md, docs/TESTING.md
- Source files: tasks/TASKS.md

## Notes
- Task 9 is deprecated; removal and renumbering will be handled under Task 15. This task focuses solely on defining the testing specification and integrating it into the planning specification.

## Features
8.1) - Author the canonical testing specification
   Action: Create docs/TESTING.md describing the philosophy, scope, structure, location, naming conventions, tooling, and workflow for tests in this project.
   Acceptance:
   - docs/TESTING.md exists and includes the following sections:
     1) Purpose and Scope
     2) Test Locations and Naming Conventions (directory layout under tasks/{task_id}/tests/, file naming, mapping to features)
     3) Test Structure and Utilities (fixtures, helpers if any, deterministic behavior requirements)
     4) Writing Acceptance Tests (how to translate acceptance criteria into tests; one-to-one mapping with feature outputs)
     5) Running Tests (local invocation via tools/run_tests, expected outputs)
     6) CI/Automation Expectations (what constitutes pass/fail gating, per-feature completion rule)
     7) Tool Usage (how the run_tests tool is used by the agent)
     8) Examples (a minimal example mapping a feature to a test file)
     9) References (PLAN_SPECIFICATION.md, TASK_FORMAT.md, TOOL_ARCHITECTURE.md)
   Context: docs/TASK_FORMAT.md, docs/PLAN_SPECIFICATION.md, docs/FEATURE_FORMAT.md, docs/TOOL_ARCHITECTURE.md
   Output: docs/TESTING.md
   Notes: This feature defines the specification only. Repository-wide test implementation is out of scope here and is addressed by future consolidation (see Task 15).

8.2) - Integrate testing into the planning specification
   Action: Update docs/PLAN_SPECIFICATION.md so testing is a mandatory part of the feature workflow and clearly referenced in the plan template.
   Acceptance:
   - docs/PLAN_SPECIFICATION.md includes a principle named "Test-Driven Acceptance" and explicitly references docs/TESTING.md.
   - The plan template shows a feature followed by its corresponding test file location and naming, making tests a mandatory deliverable.
   - Example(s) demonstrate how acceptance criteria map directly to assertions in a test file under tasks/{task_id}/tests/.
   Context: docs/PLAN_SPECIFICATION.md, docs/TESTING.md, docs/TASK_FORMAT.md
   Dependencies: 8.1
   Output: docs/PLAN_SPECIFICATION.md

8.3) - Acceptance test for 8.1: docs/TESTING.md
   Action: Write a deterministic test verifying that docs/TESTING.md exists and includes all required sections enumerated in Feature 8.1 Acceptance.
   Acceptance:
   - tasks/8/tests/test_8_1.py exists.
   - The test checks presence of docs/TESTING.md and validates required headings/keywords per 8.1.
   - Running the test suite via run_tests passes.
   Context: docs/TESTING.md, docs/PLAN_SPECIFICATION.md (Testing section), docs/TOOL_ARCHITECTURE.md
   Dependencies: 8.1
   Output: tasks/8/tests/test_8_1.py

8.4) - Acceptance test for 8.2: PLAN_SPECIFICATION updated
   Action: Write a deterministic test verifying that docs/PLAN_SPECIFICATION.md contains the "Test-Driven Acceptance" principle, references docs/TESTING.md, and that its template/example require a corresponding test per feature under tasks/{task_id}/tests/.
   Acceptance:
   - tasks/8/tests/test_8_2.py exists.
   - The test asserts presence of the phrase "Test-Driven Acceptance", a reference to "docs/TESTING.md", and template/example language requiring per-feature tests.
   - Running the test suite via run_tests passes.
   Context: docs/PLAN_SPECIFICATION.md, docs/TESTING.md
   Dependencies: 8.2
   Output: tasks/8/tests/test_8_2.py

## Execution Steps
For each feature in order:
1) Gather context (MCC) using retrieve_context_files and implement changes per Acceptance.
2) Create the test(s) that verify the feature's acceptance criteria under tasks/8/tests/.
3) Run tests using run_tests and ensure they pass.
4) Call finish_feature with a descriptive message (e.g., "Feature 8.{n} complete: {Title}") to create a per-feature commit.

After all features are completed:
5) Run run_tests again and ensure the full suite passes.
6) Update tasks/TASKS.md with status change for this task if applicable.
7) Submit for review (open PR).
8) Finish.
