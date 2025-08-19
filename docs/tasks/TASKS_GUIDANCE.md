# Task Authoring Guidance

This document provides guidance for creating well-defined, actionable tasks in the project's JSON-based format. For the definitive schema and structure, always refer to the Python type definitions in `docs/tasks/task_format.py`.

## 1. Core Principles

-   **Clarity and Conciseness**: The `title` and `action` fields should be unambiguous. Clearly state the goal and the desired outcome.
-   **Atomicity**: A task should represent a single, cohesive unit of work. If a task is too large, break it down into multiple, smaller tasks.
-   **Verifiability**: `acceptance` criteria must be clear, objective, and testable. Each criterion should describe a specific, verifiable outcome. These are the basis for the acceptance tests.

## 2. Field-by-Field Guidance

### `id` (integer)
A unique identifier for the task.

### `title` (string)
A short, descriptive title for the task (e.g., "Implement User Authentication").

### `status` (string)
The current state of the task. While the schema allows for flexibility, common statuses include `-` (Pending), `~` (In Progress), and `+` (Completed).

### `action` (string)
A  high level description of the work to be done. It should explain the 'what' and 'why' of the task.

### `plan` (string)
A step-by-step high level plan. This can help guide the development process but does not need to be exhaustive or detailed like the action field.

### `acceptance` (array)
A list of criteria that must be met for the task to be considered complete. These should be written as clear, declarative statements.

### `features` (array)
For all tasks, the work should be broken down into a list of smaller, implementable features. Each feature object within this array should follow the same principles of clarity and verifiability.

### `rejection` (string)
A user specified rejection reason. These are optional and only used if there is a specific reason why a task cannot be completed.

### `agent_question` (string)
A space for the agent to provide back a question to the user when not sure how to proceed or something else has gone wrong. This is also an optional field.

## 3. Example

For a practical example of a well-formed task, see `docs/tasks/task_example.json`.
