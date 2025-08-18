# Task Format

```
ID) STATUS Title
   Action: What needs to be done and why
   Acceptance: How to verify the task is complete
   Context: Specification files needed for this task to be completed
   Dependencies: [Optional] Tasks that must be completed first
   Output: [Optional] What artifacts/changes will be produced
   Notes: [Optional] Additional information about the task
   
   Features:
     Feature N) STATUS Title
        Action: What needs to be done and why (WHAT, not code-level HOW)
        Acceptance: How to verify this feature is complete
        Context: Specification files governing this feature
        Dependencies: [Optional]
        Output: [Optional]
        Notes: [Optional]
```

## Field Definitions

### ID
Positive integers in incremental order.

### Status
- `+` Completed - a task that is done
- `~` In Progress - a task that is being worked on
- `-` Pending - a task that requires work
- `?` Unknown - a task that requires to define what options there are and their pros and cons, after choosing an option, the task is rewritten and set to pending
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

### Context
List of files that contain detailed instructions for completing the task. Format, comma and space separate list of filenames: `SPEC_FILE.md`, `IMPLEMENTATION_GUIDE.md`

### Dependencies
Lists task IDs that must be completed before this task can begin. Format, comma and space separate list of IDs: `2, 5`

### Output
Describes what will be created or changed. Could be files, documentation, code, or process changes.

### Notes
Any extra notes about the task that explain reasoning or give extra hints about how to accomplish the task. Especially useful for `unknown` tasks that usually require a discussion.

## Features

### What is a Feature?
A Feature is a smaller, independently verifiable unit that contributes to completing a Task. Features bring precision and testability while keeping high-level details in specification documents.

- A Task is complete only when all its Features are complete (unless explicitly marked `=` Perpetual).
- Features should reference specs rather than duplicating them (Non-Redundancy Principle).

### Feature Numbering and Status
- Feature IDs are local to the Task: 1), 2), 3)...
- Status codes mirror Tasks: `+`, `~`, `-`, `?`, `/`, `=`.

### Feature Fields
Each Feature includes: Title, Action, Acceptance, Context, optional Dependencies/Output/Notes. Keep actions WHAT-focused; implementation details map to architecture specs and tools.

### Example

```
14) - Plans update
   Action: Update plans for all tasks and features.
   Acceptance: The file `docs/PLAN_SPECIFICATION.md` is updated to reflect expected behavior; `docs/SPEC.md` first action points to `docs/PLAN_SPECIFICATION.md`; `tasks/TASKS.md` reflects changes.
   Context: docs/PLAN_SPECIFICATION.md, tasks/TASKS.md, docs/SPEC.md

   Features:
     Feature 1) - Update PLAN_SPECIFICATION structure
        Action: Define how plans must cover features.
        Acceptance: PLAN_SPECIFICATION.md includes a section on feature-aware planning.
        Context: docs/PLAN_SPECIFICATION.md

     Feature 2) - Update SPEC.md ACTIONS
        Action: Make the first action to read PLAN_SPECIFICATION.md.
        Acceptance: docs/SPEC.md ACTIONS updated accordingly.
        Context: docs/SPEC.md

     Feature 3) - Align TASKS.md
        Action: Ensure tasks reflect the updated plan process.
        Acceptance: tasks/TASKS.md updated to be consistent with the plan spec.
        Context: tasks/TASKS.md
```

## Rules

### Sequential Knowledge Principle
This principle guarantees that the task list is not just a to-do list, but a readable, reproducible log of how to construct the project from its foundational principles to its final state.

### Non-Redundancy Principle
Tasks and Features should reference, not repeat, specification documents.

- **Point to the Spec:** A task or feature to implement a capability should have acceptance criteria like "The script is implemented in compliance with `SPEC_FILE.md`."
- **Specs Hold the Details:** The details of behavior belong in specification documents, not task/feature descriptions.
- **Keep Tasks/Features High-Level:** Tasks define what artifact/result to produce; Features define testable increments toward that result.

## Tips for Writing Good Tasks and Features

1. One deliverable per feature when possible
2. Concrete over abstract
3. Testable completion
4. Independent when possible

## Examples

### Simple Task
```
4) - Create specification template
   Description: Create a reusable template for writing new specifications
   Acceptance: TEMPLATE.md exists and includes all sections from SPECIFICATION_GUIDE.md. Each section holds a placeholder example.

   Features:
     Feature 1) + Define template structure
        Action: Include all required sections with examples.
        Acceptance: TEMPLATE.md has all sections with placeholders.
        Context: docs/SPECIFICATION_GUIDE.md
```

### Complex Task
```
5) - Implement specification validation
   Description: Create a tool that validates specifications against our guide
   Acceptance: Script can identify at least 3 issues in a bad spec and passes a good spec
   Dependencies: 4
   Output: validate_spec.js script

   Features:
     Feature 1) - Define validation rules
        Action: Enumerate rules derived from SPECIFICATION_GUIDE.md.
        Acceptance: Rules list exists; at least 10 rules implemented.
        Context: docs/SPECIFICATION_GUIDE.md

     Feature 2) - Implement validator script
        Action: Implement script according to rules.
        Acceptance: Script identifies >=3 issues in bad spec and passes good spec.
        Context: docs/SPECIFICATION_GUIDE.md
```
