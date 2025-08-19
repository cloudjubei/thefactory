# JSON-Based Tasks Format

## Purpose
Define the canonical, per-task JSON representation and repository layout for tasks. This format becomes the single source of truth for task data across all personas and tooling.

- Canonical Source: tasks/{id}/task.json
- Compatibility: During migration, tasks/TASKS.md is maintained as an index. See docs/TASKS_MIGRATION_GUIDE.md.
- Status Codes: Reuse definitions from docs/TASK_FORMAT.md.

## Repository Layout
Each task resides in its own folder:

- tasks/{id}/
  - task.json (canonical task data)
  - plan_{id}.md (human-readable plan following docs/PLAN_SPECIFICATION.md and docs/FEATURE_FORMAT.md)
  - tests/ (acceptance tests for this task’s features)
  - artifacts/ (optional, generated or supporting files)

## task.json Schema (conceptual)
The schema describes fields and types to be validated by JSON Schema in a follow-up task (see Task 25).

Top-level fields:
- id: integer. The task ID.
- status: string. One of "+", "~", "-", "?", "/", "=" (see docs/TASK_FORMAT.md for definitions).
- title: string. Short title of the task.
- action: string. Imperative description of the work.
- acceptance: array. Either array of strings or a structured list capturing acceptance criteria.
- notes: string (optional).
- dependencies: array of integers (optional). Task IDs.
- features: array of objects (see Feature Object below).
- metadata: object with fields:
  - created: string (ISO 8601 timestamp)
  - updated: string (ISO 8601 timestamp)
  - version: string (schema version for task.json)

Feature object fields:
- number: string. Feature ID in the form "{task_id}.{n}" (e.g., "11.1"). String is used to preserve the dot notation.
- status: string. One of "+", "~", "-", "?", "/", "=".
- title: string. Short feature title.
- action: string. What the feature implements and why.
- acceptance: array. Either array of strings or a structured list.
- context: array of strings (optional). Relevant spec/files.
- dependencies: array of strings (optional). Feature IDs like "11.2" or task IDs.
- output: array of strings (optional). Paths of created/modified artifacts.
- notes: string (optional).

Notes:
- Status codes MUST reference docs/TASK_FORMAT.md and not be redefined here.
- plan_{id}.md remains the human-readable planning document. task.json is the canonical data source.

## End-to-End Examples

### Example: Minimal task.json with one feature
```json
{
  "id": 42,
  "status": "-",
  "title": "Example Task",
  "action": "Demonstrate the JSON format by providing a minimal example.",
  "acceptance": [
    "A minimal task.json exists with required fields.",
    "Status codes reference docs/TASK_FORMAT.md."
  ],
  "dependencies": [4, 8, 10],
  "features": [
    {
      "number": "42.1",
      "status": "-",
      "title": "Create example feature",
      "action": "Add an example feature object to the task.json file.",
      "acceptance": [
        "Feature object contains the required fields."
      ],
      "context": [
        "docs/FEATURE_FORMAT.md",
        "docs/TASK_FORMAT.md"
      ],
      "output": [
        "tasks/42/task.json"
      ]
    }
  ],
  "metadata": {
    "created": "2025-08-19T00:00:00Z",
    "updated": "2025-08-19T00:00:00Z",
    "version": "1.0"
  }
}
```

### Example: Structured acceptance entries
```json
{
  "acceptance": [
    { "criterion": "docs/TASKS_JSON_FORMAT.md exists", "rationale": "Single entry-point specification." },
    { "criterion": "task.json validated against schema", "rationale": "Ensures conformance." }
  ]
}
```

## Authoring Guidance
- Use ISO 8601 timestamps for metadata.created and metadata.updated.
- Keep acceptance criteria testable; reference docs/TESTING.md for guidance.
- Prefer strings for feature.number to preserve the dotted notation.

## References
- docs/TASK_FORMAT.md (status codes, authoring rules)
- docs/FEATURE_FORMAT.md (feature structure and meaning)
- docs/PLAN_SPECIFICATION.md (planning requirements)
- docs/TASKS_MIGRATION_GUIDE.md (migration strategy and compatibility)
