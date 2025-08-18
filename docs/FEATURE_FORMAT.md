# Feature Format

## Purpose
Features are atomic, testable pieces of work that collectively satisfy a task. They define WHAT must be delivered without prescribing HOW to implement it, and they reference the project specifications rather than duplicating them.

## Format
```
{task_id}.ID) STATUS Title
   Action: What needs to be done and why
   Acceptance: Objective, testable criteria to verify completion
   Context: [Optional] Specification files (and sections) this feature relies on
   Dependencies: [Optional] Other features (e.g., 13.1) or tasks (by ID) that must be done first
   Output: [Optional] Artifacts this feature produces or changes
   Notes: [Optional] Additional clarifications
```

## Field Definitions

### ID
Positive integers in incremental order.

### Title
A succinct higher level name for the feature

### Status
- `+` Completed - a feature that is done
- `~` In Progress - a feature that is being worked on
- `-` Pending - a feature that requires work
- `?` Unknown - a feature that requires to define what options there are and their pros and cons, after choosing an option, the feature is rewritten and set to pending
- `/` Blocked - a feature that was started, but cannot proceed due to external factors
- `=` Perpetual - a feature that is always Pending, but low priority

### Acceptance
Concrete, testable conditions that define feature completion. These should be:
- **Verifiable**: Can be checked objectively
- **Specific**: No room for interpretation  
- **Complete**: When all criteria are met, the feature is done

Good acceptance criteria answers: "What must be achieved for this feature to be finished? How can this be verified?"

### Context
List of files that contain any relevant information needed for completing the feature. Format, comma and space separate list of filenames: `SPEC_FILE.md`, `IMPLEMENTATION_GUIDE.md`

### Dependencies
Lists feature IDs that must be completed before this feature can begin. Format, comma and space separate list of IDs: `1.2, 1.5`

### Output
Describes what will be created or changed. Could be files, documentation, code, or process changes.

### Notes
Any extra notes about the feature that explain reasoning or give extra hints about how to accomplish the feature. Especially useful for `unknown` features that usually require a discussion.

## Example

### Completed Feature
```
13.1) + Create the Feature Format specification
   Action: Provide a dedicated specification for describing features so plans can reference and structure them consistently.
   Acceptance:
   - docs/FEATURE_FORMAT.md exists
   - The document includes Purpose, Where Features Live, Numbering, Format, Success Criteria, and an Example
   - The format does not duplicate implementation details and references project specs when needed
   Context: docs/SPECIFICATION_GUIDE.md, docs/TASK_FORMAT.md
   Output: docs/FEATURE_FORMAT.md
   Notes: This enables consistent plan authoring across tasks.
```

### Pending Feature

### In-Progress Feature

### Unknown Feature

### Blocked Feature

### Perpetual Feature

### Pending Feature that serves as a group container for other features
