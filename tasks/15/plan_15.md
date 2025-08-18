# Plan for Task 15: Running specific tasks and features

## Intent
Add orchestrator support to run a specific task (-t) and an optional feature (-f) so the agent executes only the targeted scope, and ensure a correctly named git branch is created during submission.

## Context
- Specs: docs/SPEC.md, docs/PLAN_SPECIFICATION.md, docs/FEATURE_FORMAT.md, docs/TOOL_ARCHITECTURE.md, docs/AGENT_PRINCIPLES.md
- Source files: scripts/run_local_agent.py, tasks/TASKS.md

## Features
15.1) Add CLI selection flags to orchestrator
   Action: Add -t/--task and -f/--feature flags to scripts/run_local_agent.py. Persist selection in environment for tool usage.
   Acceptance:
   - Running the script with -t {id} and optionally -f {feature} stores selection for the session.
   - Feature requires task; providing -f without -t yields a clear error message.
   Context: docs/TOOL_ARCHITECTURE.md
   Output: Updated scripts/run_local_agent.py (argument parsing and env propagation)

15.2) Restrict execution scope via selection
   Action: Ensure the orchestrator surfaces the selection to the agent execution path so only the selected task/feature is executed.
   Acceptance:
   - Selected task/feature IDs are exported to the process environment (SELECTED_TASK_ID, SELECTED_FEATURE_ID) prior to executing tool calls.
   Context: docs/TOOL_ARCHITECTURE.md
   Output: Updated scripts/run_local_agent.py (plan execution uses selection)

15.3) Create branch with required naming during submission
   Action: Enhance submit_for_review to create/switch to a branch following the convention:
   - features/{task_id}_{feature_id} when both are provided
   - tasks/{task_id} when only task_id is provided
   Acceptance:
   - When selection is provided, the branch is created with the correct name.
   - Changes are committed (allowing empty commit) and pushed if a remote exists.
   - If GitHub CLI (gh) is available, a PR is created; otherwise, operation still succeeds without PR.
   Context: docs/TOOL_ARCHITECTURE.md
   Output: Updated scripts/run_local_agent.py (submit_for_review implementation)

## Execution Steps
1) Update scripts/run_local_agent.py to add -t/-f support, propagate selection to env, and implement branch naming in submit_for_review.
2) Update tasks/TASKS.md to mark task 15 as completed.
3) Submit for review (includes branch creation) and finish.
