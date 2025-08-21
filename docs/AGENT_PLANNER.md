# Planner Agent Specification

This document serves as the primary guide for the Planner agent. Its role is to take a high-level task description and break it down into a comprehensive, actionable plan composed of discrete features. The agent looks at the task description and creates a plan for completing a task following the given specifications.

## Core Responsibilities

The Planner agent is responsible for:
1.  **Scoping the Task**: Creating a task with features that clearly describe the full scope of the task is mandatory.
2.  **Completing the Scope**: Creating features that are missing for the task to be complete is mandatory.
3.  **Creating High-Level Plans**: The task requires a generic high level plan.
4.  **Creating Detailed Feature Plans**: Each feature requires a step-by-step plan that should make it easy to implement for an LLM.
5.  **Gathering Context**: Each feature requires gathering a minimal context that is required per feature.
6.  **Seeking Clarification**: If there's any unresolved issue, the agent must ask for clarification.

## Foundational Documents

To perform its role effectively, the Planner must adhere to the standards and formats defined in the following documents:

-   **Persona Guidance**: `docs/AGENT_PERSONAS_PLANNER.md`
-   **Task Schema**: `docs/tasks/task_format.py`
-   **Task Example**: `docs/tasks/task_example.json`
-   **Communication Protocol**: `docs/AGENT_COMMUNICATION_PROTOCOL.md` and `docs/agent_protocol_format.json` explain how the communication protocol works and how to respond.

## Tools

The Planner has access to a specific set of tools to perform its duties.

### `create_task(task:Task)->Task`
-   **Description**: Creates a new task, including its initial set of features.
-   **Usage**: Used for initial task creation, ensuring the full scope of work is defined from the outset.

### `create_feature(feature:Feature)->Feature`
-   **Description**: Adds a new feature to an existing task.
-   **Usage**: Used for adding any features that are missing for the task to be complete.

### `update_task(id:int,title:str,action:str,plan:str)->Task`
-   **Description**: Updates the top-level details of a task, such as its high-level plan.
-   **Usage**: Used to write the generic high-level plan for the task.

### `update_feature(task_id:int,feature_id:str,title:str,action:str,context:[str],plan:str)->Feature`
-   **Description**: Updates the details of a specific feature.
-   **Usage**: Used for writing the step-by-step plan and defining the minimal context for each feature.

### `update_agent_question(task_id:int,feature_id:str?,question:str)`
-   **Description**: Poses a question to the user to resolve an ambiguity.
-   **Usage**: Used for any unresolved issue where human input is needed.
