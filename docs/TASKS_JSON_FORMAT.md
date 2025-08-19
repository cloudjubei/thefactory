# JSON-based Tasks Format (Canonical)

## 1. Purpose
This document defines the canonical, JSON-based format for tasks, using a per-task folder at tasks/{id}/. It standardizes the fields stored in task.json, the structure of nested features, and required metadata. This format becomes the single source of truth for tasks post-migration (see docs/TASKS_MIGRATION_GUIDE.md).

## 2. Folder Structure
Each task lives in its own folder:

```
tasks/{id}/
  task.json              # canonical machine-readable task file
  plan_{id}.md           # human-readable plan with features and statuses
  tests/                 # acceptance tests per feature
  artifacts/             # optional: outputs, generated files, attachments
```

Key requirements:
- Folder structure: tasks/{id}/ containing task.json, plan_{id}.md, tests/, optional artifacts/.
- plan_{id}.md remains the human-readable plan and is kept in sync with task.json during migration.

## 3. task.json Schema
The task.json file captures the complete state of a task and its features.

### 3.1 Fields (Task-level)
- id (int): Unique task identifier (matches folder name).
- status (one of + ~ - ? / =): Overall task status. Status code semantics are defined in docs/TASK_FORMAT.md and must be reused here.
- title (string): Short, human-readable task title.
- action (string): The primary action the task aims to achieve.
- acceptance (array[string] or structured list): Acceptance criteria. May be a list of strings or a structured object.
- notes (string, optional): Additional freeform notes.
- dependencies (array[int], optional): IDs of tasks this task depends on.
- features (array[Feature]): A list of feature objects (see 3.2).
- metadata (object: created, updated, version): Timestamps and schema version info.

### 3.2 Feature object (Feature-level)
Each feature describes a discrete unit of work.
- number (int): Feature number within the task (e.g., for 11.3, number = 3).
- status (one of + ~ - ? / =): Feature status; same codes as docs/TASK_FORMAT.md.
- title (string): Short, human-readable feature title.
- action (string): Concrete action to perform for this feature.
- acceptance (array[string] or structured list): Criteria to verify this feature.
- context (array[string] or string): File paths or notes describing required context.
- dependencies (array[int], optional): Other feature numbers in this task that this one depends on.
- output (string, optional): Expected outputs (files/paths) produced by this feature.
- notes (string, optional): Additional freeform information.

### 3.3 Metadata
- created (string, ISO 8601): Creation timestamp for the task record.
- updated (string, ISO 8601): Last modification timestamp.
- version (string): Schema version for task.json.

## 4. Status Codes
Status codes reference and reuse the definitions from docs/TASK_FORMAT.md. Do not redefine semantics here; instead, ensure values for status and features[*].status are validated against that specification.

## 5. End-to-End Examples

### Example: task.json
```json
{
  "id": 11,
  "status": "-",
  "title": "JSON-based tasks format migration specification",
  "action": "Define and approve a new JSON-based per-task format and repository layout, plus a migration plan from tasks/TASKS.md to tasks/{id}/task.json, while preserving per-task plans in Markdown.",
  "acceptance": [
    "docs/TASKS_JSON_FORMAT.md exists and defines folder structure and schema.",
    "docs/TASKS_MIGRATION_GUIDE.md exists with migration plan and CI guidance.",
    "docs/TASK_FORMAT.md references the JSON format as canonical."
  ],
  "notes": "Documentation-only; implementation tasks follow.",
  "dependencies": [4, 8, 10],
  "features": [
    {
      "number": 1,
      "status": "-",
      "title": "Author the JSON-based tasks format specification (TASKS_JSON_FORMAT.md)",
      "action": "Create the canonical spec for task folders and task.json schema.",
      "acceptance": [
        "docs/TASKS_JSON_FORMAT.md exists.",
        "Defines folder structure and schema fields.",
        "References docs/TASK_FORMAT.md for status codes.",
        "Includes examples."
      ],
      "context": ["docs/TASK_FORMAT.md", "docs/FEATURE_FORMAT.md"],
      "dependencies": [],
      "output": "docs/TASKS_JSON_FORMAT.md",
      "notes": "Canonical source of truth for tasks after migration."
    }
  ],
  "metadata": {
    "created": "2025-01-01T00:00:00Z",
    "updated": "2025-01-01T00:00:00Z",
    "version": "1.0.0"
  }
}
```

### Example: feature entry (standalone)
```json
{
  "number": 3,
  "status": "~",
  "title": "Add schema validation to CI",
  "action": "Introduce JSON Schema files and a validation script; integrate into CI.",
  "acceptance": [
    "docs/schemas/task.schema.json and docs/schemas/feature.schema.json exist.",
    "scripts/validate_tasks_json.py validates all tasks/{id}/task.json files.",
    "CI runs validation on every PR."
  ],
  "context": ["docs/TESTING.md", "docs/TASKS_JSON_FORMAT.md"],
  "dependencies": [1],
  "output": "Validation script and passing CI run",
  "notes": "See docs/TASKS_MIGRATION_GUIDE.md for details."
}
```

## 6. Validation Guidance
- Enforce types for id, metadata timestamps, and status enumerations (+ ~ - ? / =) per docs/TASK_FORMAT.md.
- Validate features[*].number matches the position or declared number within the plan.
- Ensure acceptance is either array[string] or a structured object documented by your team.

## 7. References
- docs/TASK_FORMAT.md
- docs/PLAN_SPECIFICATION.md
- docs/TESTING.md
- docs/TASKS_MIGRATION_GUIDE.md
