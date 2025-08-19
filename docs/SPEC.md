# Problem Statement
The project defines a tool-using AI agent and supporting repository structure to execute tasks reliably. The agent must plan and implement work as atomic, testable features using a standardized JSON tool-call contract. Documentation must clearly specify how tasks, plans, features, tests, and tools interoperate so contributors (human or AI) can work consistently and safely.

# Inputs and Outputs
- Inputs:
  - Task definitions (tasks/TASKS.md and per-task plan files)
  - Project specifications (PLAN_SPECIFICATION, TESTING, TOOL_ARCHITECTURE, and related docs)
  - Source files and supporting scripts (e.g., run_local_agent.py, tools)
- Outputs:
  - Updated or newly created documentation according to acceptance criteria
  - Implemented features with passing tests
  - Per-feature commits (finish_feature) and, after all features, a submitted task (pull request)

# Constraints
- Single-cycle atomicity: one feature per execution cycle; minimal, incremental changes
- Test-driven acceptance: a feature is only done when its test exists and passes (or is paired with a subsequent testing feature as defined by the task plan)
- Tool contract: all actions are performed via the JSON schema and available tools; no hidden side effects
- Determinism: tests must be deterministic and fast; avoid external dependencies where possible
- Repository structure: docs and tasks live in predictable locations; tests for a task reside in tasks/{task_id}/tests/
- Status tracking: feature status transitions are explicit in plan files; if update_feature_status is unavailable, update the plan content directly

# Success Criteria
- Documentation and code changes satisfy the explicit acceptance criteria of the target task/feature
- Required files exist at the specified paths with the required sections/phrasing
- Tests for completed features pass using the provided test runner
- Each feature results in one isolated commit via finish_feature; after all features for the task are complete and tests pass, the task is submitted for review

# Edge Cases
- Missing or ambiguous context files: the agent must seek clarification before proceeding
- Conflicting or outdated documentation: align with PLAN_SPECIFICATION and TESTING to resolve conflicts
- Non-deterministic tests or environment-specific behavior: redesign tests to be deterministic and self-contained
- Partial implementations: do not mark features complete without corresponding passing tests or clearly linked follow-up testing features in the plan

# Examples
- A task plan enumerates features using the format {task_id}.{n} and includes Action, Acceptance, Context, Dependencies, Output, and Notes.
- A feature that creates a file includes a follow-up testing feature that verifies file existence and key section headings.
- Example of a simple test outcome expectation: a script confirms that headings "# Problem Statement", "# Inputs and Outputs", "# Constraints", "# Success Criteria", "# Edge Cases", and "# Examples" exist in a target document.
