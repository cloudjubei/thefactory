# Feature Format

## Purpose
Features are atomic, testable pieces of work that collectively satisfy a task. They define WHAT must be delivered without prescribing HOW to implement it, and they reference the project specifications rather than duplicating them.

## Where Features Live
- For each task {task_id}, features are listed inside the task plan file: tasks/{task_id}/plan_{task_id}.md.
- Optional: If a feature requires extended detail, it may get its own file under tasks/{task_id}/features/{task_id}.{n}.md.
- Keep tasks/TASKS.md high-level. Details belong in the plan and optional feature files.

## Numbering
- Use scoped numbering per task: {task_id}.{n}
  - Example: 13.2 is the second feature of Task 13.

## Feature Format
```
{task_id}.{n}) Title
   Action: What needs to be done and why
   Acceptance: Objective, testable criteria to verify completion
   Context: Specification files (and sections) this feature relies on
   Dependencies: Other features (e.g., 13.1) or tasks (by ID) that must be done first
   Output: Artifacts this feature produces or changes
   Notes: [Optional] Additional clarifications
```

## Success Criteria
Good feature acceptance criteria are:
- Binary (pass/fail)
- Measurable
- Complete
- Independent (each criterion can be validated on its own)

## Example
```
13.1) Create the Feature Format specification
   Action: Provide a dedicated specification for describing features so plans can reference and structure them consistently.
   Acceptance:
   - docs/FEATURE_FORMAT.md exists
   - The document includes Purpose, Where Features Live, Numbering, Format, Success Criteria, and an Example
   - The format does not duplicate implementation details and references project specs when needed
   Context: docs/SPECIFICATION_GUIDE.md, docs/TASK_FORMAT.md
   Dependencies: None
   Output: docs/FEATURE_FORMAT.md
   Notes: This enables consistent plan authoring across tasks.
```

## Checklist
- [ ] Numbering uses {task_id}.{n}
- [ ] Action and Acceptance are clear and testable
- [ ] Context references existing specification documents
- [ ] Outputs are explicit
- [ ] No implementation details are mandated
