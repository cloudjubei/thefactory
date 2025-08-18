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
1.  **Analysis:** Start by interpreting the task's requirements.
2.  **Creation/Modification:** Detail the primary changes to be made (e.g., creating new files, modifying existing ones).
3.  **Administration:** Include the final administrative steps, such as updating `TASKS.md` and submitting the work for review.

### 2.4. Clarity and Brevity
The plan should be easy for a human to understand. It should be concise and focus on the "what" and "why," not the low-level "how." The implementation details are found in the content of the `write_file` tool calls, not in the plan itself.

## 3. Structure
A plan is a simple, ordered list of steps. It should be written in a way that maps clearly to the subsequent `tool_calls`.

## 4. Example

For a task like:
```
12) - Plan specification
    Action: Create a plan specification that describes how each task should be executed.
    Acceptance: The file `PLAN_SPECIFICATION.md` exists and details the steps involved in creating a task plan.
```

A good corresponding plan would be:

1.  **Analyze Task:** Review Task 12 to understand the requirement is to create a specification file named `PLAN_SPECIFICATION.md`.
2.  **Draft Specification:** Formulate the content for `PLAN_SPECIFICATION.md`. The document will define the purpose, principles, structure, and provide an example of a good plan.
3.  **Update Task List:** Modify `TASKS.md` to change the status of Task 12 from `-` (Pending) to `+` (Completed).
4.  **Execute Changes:** Generate the necessary `tool_calls`:
    a. `write_file` to create `PLAN_SPECIFICATION.md` with the drafted content.
    b. `write_file` to update `TASKS.md`.
    c. `submit_for_review` to finalize the task.
    d. `finish` to end the operation.
