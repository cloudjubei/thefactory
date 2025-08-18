# Plan Specification

## 1. Purpose
A "plan" is the AI Agent's high-level, human-readable strategy for completing a given task. It is generated before any tool calls are executed. The plan outlines the agent's interpretation of the task, the steps it will take, and the final output it intends to produce. It serves as a clear statement of intent.

## 2. Core Principles
Every plan must adhere to the following principles:

### 2.1. Task-Driven
The plan must directly address the `Action` and `Acceptance` criteria of the target task from `TASKS.md`. The primary goal of the plan is to satisfy these criteria completely.

### 2.2. Atomic Execution
The plan represents a single, atomic set of actions that will be executed. The agent formulates the entire plan and all corresponding tool calls in one turn. Therefore, the plan should describe a complete unit of work, from start to finish.

### 2.3. Logical Sequence
The steps in the plan should follow a clear, logical progression:
1. **Analysis:** Start by interpreting the task's requirements.
2. **Creation/Modification:** Detail the primary changes to be made (e.g., creating new files, modifying existing ones).
3. **Administration:** Include the final administrative steps, such as updating `TASKS.md` and submitting the work for review.

### 2.4. Clarity and Brevity
The plan should be easy for a human to understand. It should be concise and focus on the "what" and "why," not the low-level "how." The implementation details are found in the content of the `write_file` tool calls, not in the plan itself.

### 2.5. Test-Driven Acceptance
A feature is not considered complete until a corresponding test is written and passes. This ensures that all work is verifiable.
- For every feature that produces a tangible output (like a file or a change in a file), a subsequent feature in the plan MUST be created to write a test for it.
- The acceptance criteria for the "test-writing" feature is simply that the test script exists and is located correctly according to `docs/TESTING.md`.
- This principle makes the acceptance criteria of the original feature concrete and machine-verifiable.

## 3. Location and Structure
- Each task MUST have a dedicated plan file located at `tasks/{task_id}/plan_{task_id}.md`.
- The plan enumerates the FEATURES that make up the task. Each feature follows `docs/FEATURE_FORMAT.md`.

A plan should include the following sections:
- Title and Task Reference
- Intent and Scope
- Context: Links to relevant specs and files
- Features: Enumerated list using `{task_id}.{n}` numbering
- Execution Steps: A short ordered list mapping to tool calls
- Administrative Steps: Update `TASKS.md`, `submit_for_review`, `finish`

## 4. Template

```
# Plan for Task {task_id}: {Task Title}

## Intent
Short, high-level description of how this plan will satisfy the task's Acceptance criteria.

## Context
- Specs: docs/SPEC.md, docs/TASK_FORMAT.md, docs/PLAN_SPECIFICATION.md, docs/FEATURE_FORMAT.md, ...
- Source files: (if any)

## Features
{task_id}.1) - Feature title
   Action: ...
   Acceptance: ...
   Context: ...
   Dependencies: ...
   Output: ...
   Notes: ...

## Execution Steps
1) Implement features and corresponding tests
2) Update `tasks/TASKS.md` with status change
3) Submit for review
4) Finish
```

## 5. Example

For a task like:
```
12) - Plan specification
    Action: Create a plan specification that describes how each task should be executed.
    Acceptance: The file `PLAN_SPECIFICATION.md` exists and details the steps involved in creating a task plan.
```

A good corresponding plan would be:

1. **Analyze Task:** Review Task 12 to confirm the goal is to create `docs/PLAN_SPECIFICATION.md` with purpose, principles, structure, and example.
2. **Draft Specification:** Author the content for `docs/PLAN_SPECIFICATION.md` covering purpose, principles, structure, template, and example.
3. **Update Task List:** Modify `tasks/TASKS.md` to change the status of Task 12 from `-` (Pending) to `+` (Completed).
4. **Execute Changes:** Generate the necessary tool calls:
   a. `write_file` to create `docs/PLAN_SPECIFICATION.md` with the drafted content.
   b. `write_file` to update `tasks/TASKS.md`.
   c. `submit_for_review` to finalize the task.
   d. `finish` to end the operation.


## Summary of execution workflow:

1. Read the task specification from `tasks/TASKS.md`.
2. Create `tasks/{task_id}/plan_{task_id}.md` and enumerate features according to `docs/FEATURE_FORMAT.md`.
3. Execute the plan, update `TASKS.md`, submit for review, and finish.
