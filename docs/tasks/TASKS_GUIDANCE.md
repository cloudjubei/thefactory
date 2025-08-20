# Task Authoring Guidance (JSON-based)

This guide describes how to author and maintain tasks using the JSON-based format. The canonical schema lives in `docs/tasks/task_format.py`. Do not duplicate schema details in docs; instead, reference the schema and focus on practical authoring guidance.

## Where tasks live
- One JSON file per task: `tasks/{task_id}/task.json`
- Tests for a task: `tasks/{task_id}/tests/`

## Required top-level fields in task.json
- `id` (int): Unique task identifier.
- `status` (str): Workflow status. Suggested values:
  - `-` Pending, `~` In Progress, `+` Done, `?` Blocked, `/` Skipped, `=` Deferred.
- `title` (str): Short, human-readable title.
- `action` (str): High-level description of the task’s purpose.
- `plan` (str, Markdown): LLM-friendly overview of how to execute the task.
- `features` (list[object]): Atomized units of work.

## Feature objects
Each feature in `features` should have:
- `id` ("{task_id}.{n}")
- `status` (same codes as tasks)
- `title` (str)
- `action` (str)
- `plan` (str, Markdown) with step-by-step, LLM-friendly guidance
- `context` (list[str]) minimal context (files) that are required to execute on this feature
- `acceptance` (list[str]) encoding verifiable criteria
- `dependencies` (list[str]) any features that must be completed before this feature can be worked on
- `rejection` (str) reasons as to why this feature is marked as rejected (e.g., “not feasible”). Can lead to rewriting spec, rewriting plan, rewriting tests and further dev work
- `agent_question` (str) place where agent puts any pending questions that need answering for the feature to be carried out
- Optional: `dependencies`, `rejection`, `agent_question`

## Example
See `docs/tasks/task_exampl.json` for an example task with features.

## Writing plans (LLM-friendly)
- Keep plans concise and structured with ordered steps.
- Focus on what/why; keep how-to implementation details in code changes.
- Include: Context files to read, primary changes to make, and administrative steps.
- Ensure every tangible change has a corresponding test feature or test file.

## Tests (required per feature that produces output)
- Location: `tasks/{task_id}/tests/`
- Naming: `test_{task_id}_{feature_number}.py`
- Tests are plain Python using stdlib only and must be deterministic.
- Each test encodes the feature’s acceptance criteria and prints clear PASS/FAIL with proper exit codes.
- Use the run tests tool via the orchestrator to verify locally.

## Workflow expectations
- One cycle = one feature = complete success.
- After implementing a feature and writing tests, run tests. When they pass, mark the feature `+` and call `finish_feature` (per-feature commit). Submit a PR only after the entire task is complete.
- The orchestrator may read tasks using helper utilities; ensure your JSON remains valid.

## References
- Canonical schema: `docs/tasks/task_format.py`
- Example: `docs/tasks/task_example.json`
- Plan spec: `docs/PLAN_SPECIFICATION.md`
- Testing spec: `docs/TESTING.md`
- Tool architecture: `docs/TOOL_ARCHITECTURE.md`
