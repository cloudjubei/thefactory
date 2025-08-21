# Developer Task Execution Specification

This document defines how the Developer agent implements features within a task. It complements persona guidance in `docs/AGENT_PERSONAS_DEVELOPER.md` and aligns with the repository tooling and workflow.

## Purpose and Scope
- Translate feature specifications into minimal, incremental code/documentation changes.
- Ensure each feature is independently testable and verifiable.
- Operate one feature per cycle, ending with a per-feature commit.

## References
- Persona: `docs/AGENT_PERSONAS_DEVELOPER.md`
- File structure: `docs/FILE_ORGANISATION.md`
- Communication protocol: `docs/AGENT_COMMUNICATION_PROTOCOL.md`, `docs/agent_protocol_format.json`
- Task schema: `docs/tasks/task_format.py`
- Planning: `docs/PLAN_SPECIFICATION.md`
- Testing guidance: `docs/TESTING.md`
- Tooling architecture: `docs/TOOL_ARCHITECTURE.md`

## Workflow
1. Select exactly one pending feature and set it In Progress.
2. Gather the minimal context required to implement the feature.
3. Implement minimal, focused changes according to the feature plan and acceptance criteria.
4. Add or update a deterministic test for this feature:
   - Location: `tasks/{task_id}/tests/`
   - File name: `test_{task_id}_{feature_number}.py`
5. Run tests and iterate until they pass.
6. Mark the feature Done and create a per-feature commit with `finish_feature`.
7. When all features in the task are Done, submit for review and finish.

## Tools
The Developer agent can use the following tools. Use them exactly as specified when available. If a tool is unavailable in your runtime, follow the provided notes.

- get_context(files:[str]) -> [str]
  - Purpose: Retrieve the content of specific files as context.
  - Note: If this tool is not available, use the orchestrator's equivalent (e.g., `retrieve_context_files`).

- write_file(filename:str, content:str)
  - Purpose: Create or overwrite files with the full content.
  - Usage: Atomic writes. Always write complete file content.

- run_test(task_id:int, feature_id:str) -> TestResult
  - Purpose: Execute tests relevant to a feature.
  - Note: If this tool is not available, use the orchestrator's `run_tests()` to run the full suite.

- update_task_status(task_id:int, status:Status) -> Task
  - Purpose: Update the overall task status (e.g., In Progress `~`, Done `+`).
  - Note: If this tool is unavailable, directly edit `tasks/{task_id}/task.json` via `write_file`.

- update_feature_status(task_id:int, feature_id:str, status:Status) -> Feature
  - Purpose: Update a specific feature's status.
  - Note: If this tool is unavailable, directly edit `tasks/{task_id}/task.json` via `write_file`.

- finish_feature(task_id:int, feature_id:str) -> Feature
  - Purpose: Create a per-feature commit once tests pass and the feature meets acceptance criteria.

- finish(task_id:int) -> Task
  - Purpose: Used when the agent has completed all work it can perform in this cycle or the entire task.

- update_agent_question(task_id:int, feature_id:str?, question:str)
  - Purpose: Escalate an unresolved issue or ambiguity that blocks progress.

Notes on tool availability and mappings:
- In some environments, tools may be exposed under different orchestrator names. For example:
  - `get_context` may be provided as `retrieve_context_files(paths: list)`.
  - `run_test` may be provided as a full-suite runner `run_tests()`.
  - `update_task_status` / `update_feature_status` may be unavailable; in that case, update `tasks/{task_id}/task.json` using `write_file`.

## Status Management
- Task and Feature statuses follow: `-` Pending, `~` In Progress, `+` Done, `?` Blocked, `/` Skipped, `=` Deferred.
- Always set the feature to `~` when starting, and to `+` only after tests pass and `finish_feature` is called.

## Testing Requirements
- Tests must be deterministic, use only the Python standard library, and clearly indicate PASS/FAIL with proper exit codes.
- Each acceptance criterion should be verifiable by the test.

## Communication Protocol
- All tool calls must be returned as a single JSON object per cycle following `docs/AGENT_COMMUNICATION_PROTOCOL.md` and the format in `docs/agent_protocol_format.json`.
- Provide a concise plan and a list of tool calls; avoid additional prose output outside the JSON schema.
