# Task 11 Plan: JSON-based Tasks Format and Migration

This plan follows docs/PLAN_SPECIFICATION.md and docs/TASK_FORMAT.md. It defines a staged migration to a JSON-based per-task format with dual-read compatibility, orchestrator/tooling updates, and full repository migration.

11.1) - Define typed interfaces and guidance
Action: Author the canonical typed interfaces for tasks/features and move the guidance doc.
Acceptance:
- docs/tasks/task_format.py exists and defines fully typed Python 3.11 dataclass interfaces and Enums:
  - Task, Feature, TaskStatus (Enum), FeatureStatus (Enum), Context, Output, AcceptanceCriteria, Rejection.
  - Serialization to/from JSON is demonstrated for Task and Feature.
- docs/tasks/task_example.json exists and validates against the interfaces by round-trip (load->dump->load) in tests.
- docs/TASK_FORMAT.md is moved to docs/tasks/TASKS_GUIDANCE.md (content updated to reference the JSON format; no duplication of fields already defined by task_format.py).
- All new references point to docs/tasks/TASKS_GUIDANCE.md; no broken links introduced (verified by tests).
- Tests exist under tasks/11/tests/ validating:
  - Enum values and required fields.
  - Round-trip serialization fidelity using task_example.json.
  - Link checker for moved guidance doc.
Context: docs/TASK_FORMAT.md, docs/TOOL_ARCHITECTURE.md, docs/PLAN_SPECIFICATION.md.
Dependencies: None.
Output: docs/tasks/task_format.py, docs/tasks/task_example.json, docs/tasks/TASKS_GUIDANCE.md; unit tests in tasks/11/tests/.
Notes: Use Python 3.11 dataclasses + typing + Enum; avoid external deps.

11.2) - Update orchestrator and tool contracts for dual-read and feature tools
Action: Update scripts/run_local_agent.py to support dual-read (Markdown and JSON) and wire new tools to the JSON sources.
Acceptance:
- scripts/run_local_agent.py can read tasks from tasks/TASKS.md and tasks/{id}/task_{id}.json (dual-read).
- Tools read_plan_feature and update_feature_status are implemented and exposed, operating on the JSON format.
- docs/TOOL_ARCHITECTURE.md updated to reflect the JSON-backed behavior and any argument nuances.
- Backward compatibility proven by tests running in both modes.
- Tests exist under tasks/11/tests/ covering dual-read selection and tool behavior against sample JSON.
Context: scripts/run_local_agent.py, docs/TOOL_ARCHITECTURE.md, docs/AGENT_PRINCIPLES.md.
Dependencies: 11.1
Output: Updated scripts/run_local_agent.py; updated docs/TOOL_ARCHITECTURE.md; tests under tasks/11/tests/.
Notes: Preserve current behavior for Markdown during migration.

11.3) - Implement scripts/tools/get_task_and_feature.py
Action: Create a utility to load a Task and optionally select a Feature.
Acceptance:
- scripts/tools/get_task_and_feature.py exists with functions:
  - load_task(task_id: int) -> Task
  - select_feature(task: Task, feature_number: int | None) -> Feature | None
- Proper error handling and typing annotations present.
- Unit tests under tasks/11/tests/ cover happy paths and errors.
Context: docs/tasks/task_format.py, docs/tasks/task_example.json.
Dependencies: 11.1
Output: scripts/tools/get_task_and_feature.py; tests under tasks/11/tests/.
Notes: The loader must validate required fields and enums.

11.4) - Author the migration guide
Action: Write docs/tasks/TASKS_MIGRATION_GUIDE.md with a safe, stepwise migration.
Acceptance:
- The guide includes: stepwise dual-read migration, orchestrator/context selection for personas, test/CI implications referencing docs/TESTING.md, rollback plan, deprecation timeline for TASKS.md.
- Cross-references to docs/tasks/TASKS_GUIDANCE.md and docs/tasks/task_format.py.
- Link check tests under tasks/11/tests/ pass.
Context: docs/TESTING.md, docs/PLAN_SPECIFICATION.md, docs/TOOL_ARCHITECTURE.md.
Dependencies: 11.1, 11.2
Output: docs/tasks/TASKS_MIGRATION_GUIDE.md; tests under tasks/11/tests/.
Notes: Emphasize that TASKS.md removal is last step only when all tasks are migrated.

11.5) - Pilot migration for Tasks 1–4
Action: Migrate tasks 1–4 to the JSON format and new folder structure.
Acceptance:
- For each task (1–4): tasks/{id}/task_{id}.json, tasks/{id}/task_plan_{id}.md, tasks/{id}/features/feature_plan_{id}_{feature_id}.md, and tests under tasks/{id}/tests/ exist and validate.
- Dual-read remains enabled; TASKS.md entries persist but may note the migration state.
- Tests validate JSON schema via interfaces and basic plan/test file presence.
Context: Existing tasks/plans/tests for 1–4, docs/tasks/task_format.py, docs/TESTING.md.
Dependencies: 11.1, 11.2, 11.3, 11.4
Output: New per-task JSON and plan/test files for tasks 1–4; tests under tasks/11/tests/ and/or per-task tests.
Notes: Keep content fidelity; no scope changes.

11.6) - Full migration and removal of TASKS.md
Action: Migrate remaining tasks, update references, and remove tasks/TASKS.md.
Acceptance:
- All remaining tasks fully migrated to the JSON structure and folder layout.
- All references to docs/TASK_FORMAT.md are updated to docs/tasks/TASKS_GUIDANCE.md.
- scripts/run_local_agent.py defaults to JSON and retains optional Markdown fallback guarded by a feature flag until removal commit.
- TASKS.md is removed in this feature commit, after all tests pass and CI validates the repository in JSON-only mode.
- Final tests confirm loading all tasks, selecting features, and passing link checks.
Context: Entire repository.
Dependencies: 11.1, 11.2, 11.3, 11.4, 11.5
Output: Migration commits across tasks; removal of tasks/TASKS.md; updated references; tests.
Notes: Perform as a discrete, reviewable final feature.
