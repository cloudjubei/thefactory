# Task 13 – JSON-based tasks format

Intent: Define and roll out a JSON-based format for tasks that supersedes TASKS.md, including schema, examples, tooling, migration/integration steps, and cleanup. Plans here are concise, LLM-friendly, and structured per FEATURE_FORMAT. For the canonical schema and storage, see docs/tasks/task_format.py and tasks/13/task.json.

Execution Protocol (per PLAN_SPECIFICATION):
- One Cycle = One Feature = Complete Success
- For each feature: gather MCC, implement, write tests in tasks/13/tests/, run tests, finish_feature, then proceed.
- After all features pass: update task status to + and submit for review.

Context Specs:
- docs/PLAN_SPECIFICATION.md
- docs/FEATURE_FORMAT.md
- docs/tasks/TASKS_GUIDANCE.md

Features

13.1) + Define Task Schema in Python
   Action: Create docs/tasks/task_format.py defining Python types (Task, Feature, etc.) as the canonical schema.
   Acceptance:
   - docs/tasks/task_format.py exists.
   - Defines Python types for Task, Feature, and related data structures.
   - Covers all fields used in TASKS.md and plan.md files.
   Context: docs/PLAN_SPECIFICATION.md, docs/FEATURE_FORMAT.md
   Output: docs/tasks/task_format.py
   Plan:
   - Implement TypedDict/dataclasses for Task and Feature with strict fields.
   - Ensure parity with existing fields and new plan field.
   - Add inline docs.
   Notes: Marked complete; verify with a test that the file exists and types are defined.

13.2) + Create Example JSON Task File
   Action: Create docs/tasks/task_example.json demonstrating a complete task conforming to the schema.
   Acceptance:
   - docs/tasks/task_example.json exists.
   - JSON is valid and conforms to docs/tasks/task_format.py.
   Dependencies: 13.1
   Output: docs/tasks/task_example.json
   Plan:
   - Author a representative example covering all fields.
   - Validate with a simple loader/validator test.
   Notes: Marked complete; ensure there is a test that checks existence and structure.

13.3) - Update Task Authoring Guidance
   Action: Move docs/TASK_FORMAT.md to docs/tasks/TASKS_GUIDANCE.md and update content to align with JSON format; remove schema details now covered by task_format.py; focus on authoring best practices.
   Acceptance:
   - docs/tasks/TASKS_GUIDANCE.md exists.
   - Content reflects JSON-based workflow.
   - docs/TASK_FORMAT.md is removed.
   - docs/FEATURE_FORMAT.md is removed.
   Dependencies: 13.1
   Output: docs/tasks/TASKS_GUIDANCE.md
   Plan:
   - Migrate/rename file, update content to reference task_format.py.
   - Remove redundant schema sections; emphasize authoring guidance.
   - Add tests verifying file presence/absence as per acceptance.

13.4) - Create Task Utility Tooling
   Action: Create scripts/tools/task_utils.py to read/create/update tasks in the new JSON format; abstract task I/O.
   Acceptance:
   - scripts/tools/task_utils.py exists.
   - Uses docs/tasks/task_format.py types.
   - Functions: get_task(task_id), update_task(task_id, task_data), create_task(...), update_task_status(task_id, feature_id?, status), ask_agent_question().
   - Centralizes all task/feature edits; documented with error handling.
   Dependencies: 13.1, 13.2
   Output: scripts/tools/task_utils.py
   Plan:
   - Implement typed helpers for robust JSON read/write and status updates.
   - Replace direct editing with these utilities; include docstrings and exceptions.
   - Tests: verify functions and safe I/O behavior.

13.5) - Integrate Tooling into Orchestrator
   Action: Update run_local_agent.py to use task_utils.py for task operations.
   Acceptance:
   - run_local_agent.py imports and uses task_utils.py.
   - Orchestrator can parse task info from the new JSON structure.
   Dependencies: 13.4
   Output: Modified scripts/run_local_agent.py
   Plan:
   - Swap existing task access points for task_utils functions.
   - Validate single-feature execution flow remains intact.
   - Tests: ensure orchestrator reads task.json and executes per-feature.

13.6) - The plan field should be updated
   Action: Ensure plan fields for tasks and features are Markdown, LLM-friendly, and stepwise.
   Acceptance:
   - Each task and feature has a filled plan field.
   - Each plan field is Markdown.
   - Plans are clear, concise, and step-structured for AI execution.
   Dependencies: 13.5
   Plan:
   - Populate plan in tasks/*/task.json and feature entries.
   - Tests: spot-check representative tasks for plan presence/format.

13.7) - Cleanup
   Action: Handle remaining functionality gaps and repository cleanup for the new format.
   Acceptance:
   - Completed tasks have status '+'.
   - Task folders contain tests/ and task.json only.
   - Deprecation/cleanup features removed.
   - Non-applicable features refined or removed.
   Dependencies: 13.6
   Plan:
   - Normalize task folders; remove stale files.
   - Tests: verify folder structure and statuses.

13.8) - Migrate to task 1
   Action: Consolidate all task-format definitions under Task 1 as the canonical source; Task 13 remains as documentation.
   Acceptance:
   - Relevant information migrated into Task 1.
   - Task 13 becomes superfluous but preserved as doc.
   Dependencies: 13.7
   Plan:
   - Move/merge definitions and references to Task 1.
   - Tests: verify Task 1 contains all relevant definitions.

Notes
- Testing: For each feature, add tasks/13/tests/test_13_{n}.py verifying acceptance (existence, structure, behavior) and run via run_tests.
- Commit protocol: Use finish_feature per feature after tests pass; submit_for_review only after all features complete.
