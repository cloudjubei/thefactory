# Repository File Organisation

- tasks/{id}/task.json: Canonical source of truth for each task, including title, action, acceptance, and embedded plans for the task and each feature.
- tasks/{id}/tests/: Tests for that task's features.
- docs/: Specifications and guidance for authoring tasks and features.
- scripts/: Orchestrator and tool implementations.

Notes:
- plan.md files are deprecated and must not be used. All plans are embedded as Markdown in the `plan` field within task.json.
- During migration, legacy references may exist in history, but current tooling and docs assume the JSON format only.
