Reference: This document follows docs/SPECIFICATION_GUIDE.md for structure and rigor.

# WHAT
- Purpose: Define the entry-point specification for a tool-using AI agent project. The project organizes work as tasks composed of atomic, testable features executed via a safe JSON tool-call contract. This document orients contributors to what the project is and how it operates at a high level.
- Scope: Provide a concise overview and pointers to canonical documents so contributors can start effectively. The detailed rules live in the referenced specifications (see CORE IDEAS and ACTIONS).

Inputs
- Task definitions (tasks/TASKS.md) and per-task plans (tasks/{task_id}/plan_{task_id}.md)
- Project specifications and guides (docs/PLAN_SPECIFICATION.md, docs/TASK_FORMAT.md, docs/FEATURE_FORMAT.md, docs/TOOL_ARCHITECTURE.md, docs/AGENT_PRINCIPLES.md, docs/TESTING.md)
- Orchestrator and tools (scripts/run_local_agent.py and tools under scripts/tools)

Outputs
- Updated or newly created documentation/files according to acceptance criteria
- Implemented features with passing tests and per-feature commits (finish_feature)
- A submitted task (pull request) once all features for that task are complete

# CORE IDEAS
- Agent vs Orchestrator: The LLM is the Agent (the intelligence); the local script (run_local_agent.py) is the Orchestrator (the executor). See docs/AGENT_PRINCIPLES.md.
- Tool Contract: All actions are executed via a strict JSON schema and safe tools. See docs/TOOL_ARCHITECTURE.md for the schema and available tools.
- Single-Feature Focus: One feature per execution cycle to ensure predictability, debuggability, and complete testing.
- Task/Plan/Feature Structure: Tasks live in tasks/TASKS.md; each task has a plan describing features under tasks/{task_id}/plan_{task_id}.md. See docs/TASK_FORMAT.md and docs/PLAN_SPECIFICATION.md; feature field definitions are in docs/FEATURE_FORMAT.md.
- Status Tracking: Use standardized status symbols for both tasks and features as defined in docs/TASK_FORMAT.md. Update statuses precisely.
- Test-Driven Acceptance: A feature is complete only when its acceptance criteria are verified by deterministic tests. See docs/TESTING.md.
- Determinism: Tests must be deterministic, fast, and self-contained; avoid external, flaky dependencies.
- Non-Redundancy: Keep a single source of truth; reference canonical docs rather than duplicating content. See docs/TASK_FORMAT.md (Rules: Non-Redundancy).
- Context-First: Gather all relevant files/specs before changing anything; when context is missing or ambiguous, ask a clarifying question.
- Edge Cases (operational):
  - Missing or ambiguous context: pause and ask a question before proceeding
  - Conflicting documentation: align to PLAN_SPECIFICATION and TESTING
  - Partial implementations: do not mark complete without tests (or explicit plan sequencing when legacy tasks defer tests)

# ACTIONS
1) Read the core specs to understand expectations:
   - docs/SPECIFICATION_GUIDE.md (spec rigor)
   - docs/TASK_FORMAT.md, docs/PLAN_SPECIFICATION.md, docs/FEATURE_FORMAT.md (task/plan/feature rules)
   - docs/TOOL_ARCHITECTURE.md (tool contract, JSON schema, available tools)
   - docs/AGENT_PRINCIPLES.md (roles and principles)
   - docs/TESTING.md (testing requirements)
2) Select a pending task from tasks/TASKS.md and open its plan at tasks/{task_id}/plan_{task_id}.md.
3) Gather context listed in the feature’s Context section. Read existing files that will be created or modified.
4) Execute exactly one feature per cycle:
   - Implement minimal, necessary changes via write_file
   - Create or update tests under tasks/{task_id}/tests/ to cover acceptance
   - Run tests (run_tests) and fix issues until passing
   - Commit using finish_feature once acceptance is satisfied
5) Update statuses accurately in plan and tasks/TASKS.md as needed, following docs/TASK_FORMAT.md.
6) After all features of a task are complete and tests pass, submit the task for review (submit_for_review) and finish the cycle (finish).
7) If requirements are ambiguous or decisions exceed scope, use ask_question to request clarification before proceeding.