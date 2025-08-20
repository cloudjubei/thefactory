# Feature Format Specification

This document defines the structure and authoring guidance for features within a task's task.json file.

1) Feature Object Structure
- id: string in the form "{task_id}.{n}" (e.g., "13.9").
- status: one of '+', '~', '-', '?', '/', '='.
- title: short human-readable title.
- action: one-sentence description of what to implement.
- acceptance: list of acceptance criteria strings or phased blocks.
- plan: Markdown content describing the step-by-step plan for this feature. This plan must be LLM-friendly: clear, concise, and logically ordered so an agent can execute it directly. Use headings, lists, and short sentences.
- dependencies: optional list of feature IDs this feature depends on.
- output: optional description of expected artifacts/paths.
- notes: optional freeform notes, including audit trail entries.

2) Plan Field Requirements (LLM-friendly Markdown)
- Use Markdown headings and bulleted or numbered lists.
- Keep steps short, action-oriented, and ordered.
- Include references to files and tools by relative path and exact tool names.
- Avoid ambiguity; prefer concrete checks tied to acceptance.
- Keep the plan within the feature focused on a single cohesive change.

3) Location
- All features live inside tasks/{task_id}/task.json under the "features" array.
- Plans are embedded; plan.md files are deprecated and must not be referenced.

4) Example
```
{
  "id": "99.1",
  "status": "-",
  "title": "First Feature",
  "action": "Create the initial specification file.",
  "acceptance": [
    "docs/SPEC.md exists and includes the heading 'Specification'."
  ],
  "plan": """
### Intent
Implement the spec file as per acceptance.

### Steps
1. Create docs/SPEC.md with required heading.
2. Write tasks/99/tests/test_99_1.py to validate.
3. Run tests; if pass, finish_feature.
"""
}
```

5) Status Updates
- Use the update_feature_status tool to change status atomically during execution cycles.
