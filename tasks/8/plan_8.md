# Plan for Task 8: Tests specification

## Intent
Establish the canonical, project-wide testing specification and integrate test requirements into the planning specification so every feature is verifiable by deterministic tests.

## Context
- docs/TASK_FORMAT.md
- docs/PLAN_SPECIFICATION.md
- docs/TOOL_ARCHITECTURE.md

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
   Output: docs/TESTING.md

8.2) - Integrate testing into the planning specification
   Action: Update docs/PLAN_SPECIFICATION.md so testing is a mandatory part of the feature workflow and clearly referenced in the plan template.
   Acceptance:
   - docs/PLAN_SPECIFICATION.md includes a principle named "Test-Driven Acceptance" and explicitly references docs/TESTING.md.
   - The plan template shows a feature followed by its corresponding test file location and naming, making tests a mandatory deliverable.
   - Example(s) demonstrate how acceptance criteria map directly to assertions in a test file under tasks/{task_id}/tests/.
   Context: docs/PLAN_SPECIFICATION.md, docs/TESTING.md, docs/TASK_FORMAT.md
   Dependencies: 8.1
   Output: docs/PLAN_SPECIFICATION.md

## Notes
- This task defines the specification; it does not implement or modify existing tests.
- Task 9 (Automated tests) remains responsible for implementing tests and ensuring they pass; Task 15 may later restructure/merge tasks, but this plan keeps scope limited to specification.

## Execution Steps
1) Implement features (by appropriate personas) following Context and Acceptance.
2) Update tasks/TASKS.md to reflect feature/task status changes during execution.
3) Submit for review.
4) Finish.
