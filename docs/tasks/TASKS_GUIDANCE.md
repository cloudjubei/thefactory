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
- `acceptance` (list[object]|optional): Optional structured acceptance checklist.
- `features` (list[object]): Atomized units of work.

See `docs/tasks/task_format.py` for the definitive schema and optional fields.

## Feature objects
Each feature in `features` should have:
- `id` ("{task_id}.{n}")
- `status` (same codes as tasks)
- `title` (str)
- `action` (str)
- `acceptance` (list[str]) encoding verifiable criteria
- `plan` (str, Markdown) with step-by-step, LLM-friendly guidance
- Optional: `dependencies`, `context`, `output`, `notes`

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

## Deprecations
- The legacy markdown files `docs/TASK_FORMAT.md` and `docs/FEATURE_FORMAT.md` are removed in favor of this guidance and the canonical schema in `docs/tasks/task_format.py`.

## References
- Canonical schema: `docs/tasks/task_format.py`
- Plan spec: `docs/PLAN_SPECIFICATION.md`
- Testing spec: `docs/TESTING.md`
- Tool architecture: `docs/TOOL_ARCHITECTURE.md`
