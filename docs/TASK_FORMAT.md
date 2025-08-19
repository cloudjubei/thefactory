# Task Format

```
ID) STATUS Title
   Action: High level description of what needs to be done
   Acceptance: High level description of how to verify the task is complete
   Notes: [Optional] Additional information about the task
   Rejection: [Optional] Information about why this task is currently being rejected
```

## Field Definitions

### ID
Positive integers in incremental order.

### Title
A succinct higher level name for the task

### Status
- `+` Completed - a task that is done
- `-` Pending - a task that requires work, i.e. at least one feature is Pending
- `~` In Progress - a task that is being worked on, supercedes Pending, i.e. at least one feature is In Progress
- `?` Unknown - a task that has unknowns, supercedes In Progress, i.e. at least one feature is Unknown
- `/` Blocked - a task that has been blocked, supercedes Unknown, i.e. at least one feature is Blocked
- `=` Perpetual - a task that has no end date, i.e. at least one feature is Perpetual and all other features are Completed

### Action
A clear explanation of what needs to be accomplished. Should be specific enough that someone unfamiliar with the project can understand the task.

### Acceptance
Concrete, testable conditions that define task completion. These should be:
- **Verifiable**: Can be checked objectively
- **Specific**: No room for interpretation  
- **Complete**: When all criteria are met, the task is done

Good acceptance criteria answers: "What must be achieved for this task to be finished? How can this be verified?"

### Notes
Any extra notes about the task that explain reasoning or give extra hints about how to accomplish the task. Especially useful for `unknown` tasks that usually require a discussion.

### Rejection
Concrete reason that defines why the task is not accepted.
If the reason introduces new spec that isn't already covered elsewhere, add it to the spec.

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
   Action: Create a reusable template for writing new specifications
   Acceptance: TEMPLATE.md exists and includes all sections from SPECIFICATION_GUIDE.md. Each section holds a placeholder example.
```


### In-Progress Task
```
6) ~ Document existing specifications
   Action: Find and document 3 real-world specification examples
   Acceptance: EXAMPLES/ directory contains 3 .md files with annotated specifications
```

## Tips for Writing Good Tasks

1. **One high-level deliverable per task** - If you need multiple outputs, create multiple tasks
2. **Concrete over abstract** - "Create X file" not "Improve documentation"
3. **Testable completion** - Anyone should be able to verify if it's done

