# Tasks Migration Guide: From TASKS.md to task.json

## Overview
This guide defines the stepwise migration from a monolithic tasks/TASKS.md to per-task folders with a canonical tasks/{id}/task.json, preserving plan_{id}.md and tests. It ensures backward compatibility during migration and sets expectations for tooling, testing, rollback, and deprecation.

Dependencies: Task 4 (Plan spec), Task 8 (Testing spec), Task 10 (Agent personas)

## Goals
- Establish task.json as the canonical source of truth for task metadata and features.
- Maintain dual-read compatibility (TASKS.md and task.json) during migration.
- Provide minimal, persona-scoped context to agents.
- Integrate schema validation into tests/CI.
- Define rollback and deprecation strategy for TASKS.md.

## Migration Steps (High-Level)
1) Define JSON format (this task)
   - Create docs/TASKS_JSON_FORMAT.md and update docs/TASK_FORMAT.md to reference JSON as canonical.
2) Implement schemas and validation tooling (Task 25)
   - Create JSON Schemas: docs/schemas/task.schema.json and docs/schemas/feature.schema.json.
   - Provide scripts/validate_tasks_json.py to validate all task.json files.
   - Integrate into tests/CI. See docs/TESTING.md.
3) Update orchestrator for task.json (Task 26)
   - Update scripts/run_local_agent.py to load tasks/{id}/task.json.
   - Enforce persona-scoped context loading per docs below.
   - Maintain backward compatibility by supporting TASKS.md until migration ends.
4) Migrate existing tasks (Task 27)
   - For each task: create tasks/{id}/task.json; ensure plan_{id}.md exists; link features and tests.
   - Pass validation via the schema tooling.
5) Remove legacy TASKS.md (Task 28)
   - Remove tasks/TASKS.md after successful migration.
   - Update docs to rely solely on JSON-based format.

## Dual-Read Backward Compatibility
- Authoring: During migration, authors may update both task.json and TASKS.md for visibility.
- Orchestrator: Attempt to read tasks/{id}/task.json first; if absent, fall back to parsing tasks/TASKS.md.
- Display: Tools and scripts should prefer task.json when present.
- Termination: Dual-read ends with Task 28 completion.

## Tooling Requirements: Orchestrator and Context Selection
To minimize context per persona and per feature:
- Persona-scoped context (see scripts/run_local_agent.py):
  - Manager: tasks/TASKS.md or tasks/{id}/task.json, docs/TASK_FORMAT.md, docs/TOOL_ARCHITECTURE.md.
  - Planner: tasks/{id}/task.json, tasks/{id}/plan_{id}.md, docs/PLAN_SPECIFICATION.md, docs/FEATURE_FORMAT.md, docs/TASK_FORMAT.md.
  - Tester: tasks/{id}/task.json, tasks/{id}/tests/, docs/TESTING.md.
  - Developer: tasks/{id}/task.json, tasks/{id}/plan_{id}.md, relevant source files, docs/PLAN_SPECIFICATION.md, docs/TESTING.md, docs/TOOL_ARCHITECTURE.md.
- Feature-scoped loading: load only files listed in the feature's Context plus the plan file and target outputs.
- Backward compatibility: if task.json is missing, derive minimal context from TASKS.md.

## Test Impact and CI Updates
- Schema Validation (Task 25):
  - Add docs/schemas/task.schema.json and docs/schemas/feature.schema.json.
  - Introduce scripts/validate_tasks_json.py to validate all tasks/{id}/task.json.
  - CI: Run validation script on every PR; fail on schema violations.
- Tests Location and Structure: Continue placing tests under tasks/{id}/tests/ (see docs/TESTING.md).
- Acceptance Encoding: Ensure acceptance criteria from task.json are reflected in tests; avoid "test-only" features per docs/TESTING.md.

## Rollback Plan
- If issues arise, retain dual-read by continuing to maintain TASKS.md; open a revert PR restoring the prior behavior.
- Keep migration changes isolated per task to enable selective rollback.
- Document any partial migrations per task in a MIGRATION_STATUS.md (optional) until completion.

## Deprecation Strategy for TASKS.md
- During migration: TASKS.md remains as a compatibility index and overview.
- After Task 28: Remove TASKS.md; update documentation to reference the JSON format exclusively.
- Enforce through CI by validating presence of task.json for all active tasks.

## References
- docs/TASKS_JSON_FORMAT.md (canonical JSON format)
- docs/TASK_FORMAT.md (status codes, rules, and authoring tips)
- docs/PLAN_SPECIFICATION.md (planning model and feature cadence)
- docs/FEATURE_FORMAT.md (feature data definitions)
- docs/TESTING.md (testing requirements and CI expectations)
- scripts/run_local_agent.py (orchestrator and persona modes)
