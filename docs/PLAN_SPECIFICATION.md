# Plan Specification

This document outlines the purpose, principles, structure, and lifecycle of plans used by the AI agent to execute tasks.

## 1. Purpose
The `plan` is the agent's strategy for completing a task, formulated before execution. It is stored within the `task.json` file and outlines the agent's interpretation of the task, the steps it will take, and the intended final output.

## 2. Core Principles
- **Task-Driven**: The plan must directly address the `action` and `acceptance` criteria of the task.
- **Logical Sequence**: Steps should follow a logical progression: analysis, implementation, testing, and administration.
- **Clarity and Brevity**: The plan should be concise and human-readable, focusing on the 'what' and 'why,' not the low-level 'how.'

## 3. Structure
Each task's definition is located at `tasks/{task_id}/task.json`. This is the single source of truth for the task's scope and execution strategy.

- **Mandatory Scope**: A task must be created with features that clearly describe its full scope.
- **High-Level Plan**: The top-level `plan` field in the task must contain a generic, high-level plan for the entire task.
- **Feature Plan**: Each feature must have its own `plan` field containing a step-by-step guide that is easy for an LLM to implement.
- **Acceptance Criteria**: Each feature must have rigorous `acceptance` criteria, which form the basis for writing deterministic tests.

## 4. Task and Feature Lifecycle

1.  **Creation**: A task is defined in `tasks/{task_id}/task.json` with a high-level plan and a complete set of features that scope the entire task.
2.  **Execution**: The agent works on one feature at a time.
3.  **Status Updates**: As the agent works, it updates the `status` of the feature and the overall task in the `task.json` file by using the `write_file` tool.
4.  **Testing**: For every feature that produces a tangible output, a test must be written and must pass.
5.  **Feature Completion**: A feature is only considered complete after its tests pass and the agent has called the `finish_feature` tool to commit the work for that feature.
6.  **Task Completion**: Once all features are complete, the agent calls `submit_for_review` to open a pull request, followed by the `finish` tool to end the cycle.

## 5. References
- **Task Schema**: `docs/tasks/task_format.py`
- **Task Example**: `docs/tasks/task_example.json`
- **Task Guidance**: `docs/tasks/TASKS_GUIDANCE.md`
- **Testing Guidance**: `docs/TESTING.md`
- **Tooling Guidance**: `docs/TOOL_ARCHITECTURE.md`
- **Agent Principles**: `docs/AGENT_PRINCIPLES.md`
- **Agent Personas**: `docs/AGENT_PERSONAS.md`
