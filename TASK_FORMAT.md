# Task Format

```
ID) STATUS Title
   Action: What needs to be done and why
   Acceptance: How to verify the task is complete
   Dependencies: [Optional] Tasks that must be completed first
   Output: [Optional] What artifacts/changes will be produced
   Notes: [Optional] Additional information about the task
```

## Field Definitions

### ID
Positive integers in incremental order.

### Status
- `+` Completed - a task that is done
- `~` In Progress - a task that is being worked on
- `-` Pending - a task that requires work
- `?` Unknown - a task that is unclear, requires clarification of further discussion
- `/` Blocked - a task that was started, but cannot proceed due to external factors
- `=` Perpetual - a task that is always Pending, but low priority

### Title
A succinct higher level name for the task

### Action
A clear explanation of what needs to be accomplished. Should be specific enough that someone unfamiliar with the project can understand the task.

### Acceptance
Concrete, testable conditions that define task completion. These should be:
- **Verifiable**: Can be checked objectively
- **Specific**: No room for interpretation  
- **Complete**: When all criteria are met, the task is done

Good acceptance criteria answers: "How do I know this task is finished?"

### Dependencies
Lists task IDs that must be completed before this task can begin. Format, comma and space separate list of IDs: `2, 5`

### Output
Describes what will be created or changed. Could be files, documentation, code, or process changes.

## Rules

### Sequential Knowledge Principle
This principle guarantees that the task list is not just a to-do list, but a readable, reproducible log of how to construct the project from its foundational principles to its final state.

### Non-Redundancy Principle
Tasks should reference, not repeat, specification documents.

- **Point to the Spec:** A task to implement a feature (e.g., "Implement the Orchestrator") should have an acceptance criterion like "The script is implemented in compliance with `SPEC_FILE.md`."
- **Specs Hold the Details:** The details of implementation (e.g., specific function names, arguments, class structures) belong in the specification documents, not in the task descriptions.
- **Keep Tasks High-Level:** Tasks define *what* artifact to produce, while specifications define *how* that artifact must behave.

## Examples

### Simple Task
```
4) - Create specification template
   Description: Create a reusable template for writing new specifications
   Acceptance: TEMPLATE.md exists and includes all sections from SPECIFICATION_GUIDE.md. Each section holds a placeholder example.
```

### Complex Task
```
5) - Implement specification validation
   Description: Create a tool that validates specifications against our guide
   Acceptance: Script can identify at least 3 issues in a bad spec and passes a good spec
   Dependencies: 4
   Output: validate_spec.js script
```

### In-Progress Task
```
6) ~ Document existing specifications
   Description: Find and document 3 real-world specification examples
   Acceptance: EXAMPLES/ directory contains 3 .md files with annotated specifications
   Output: EXAMPLES/ directory with README.md
```

## Tips for Writing Good Tasks

1. **One deliverable per task** - If you need multiple outputs, create multiple tasks
2. **Concrete over abstract** - "Create X file" not "Improve documentation"
3. **Testable completion** - Anyone should be able to verify if it's done
4. **Independent when possible** - Minimize dependencies to allow parallel work