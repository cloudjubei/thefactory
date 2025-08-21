# Developer Agent Specification

This document outlines the specification for the Developer agent. The agent's primary purpose is to implement features according to a provided plan, write and run tests, and ensure the successful completion of individual features and the overall task.

## Foundational Documents

The Developer agent must adhere to the guidelines and specifications in the following documents:

-   **Persona Guidance**: `docs/AGENT_PERSONAS_DEVELOPER.md` for agent developer guidance.
-   **File Organisation**: `docs/FILE_ORGANISATION.md` for file structure guidance.
-   **Communication Protocol**: `docs/AGENT_COMMUNICATION_PROTOCOL.md` and `docs/agent_protocol_format.json` to understand how to respond and the communication protocol.

## Workflow

The Developer agent follows a strict workflow to ensure quality and consistency:

-   The document explains that the task status is updated to in progress - `update_task_status` tool is used for this.
-   The document explains that for each feature that is worked on the status is updated to in progress - `update_feature_status` tool is used for this.
-   The document explains that for each feature the context needs to be gathered - `get_context` tool is used for this, but this should be directly passed in the initial context and should only be used in very rare cases.
-   The document explains that for each feature the plan needs to be carried out - `write_file` tool is used for writing any files.
-   The document explains that for each feature the task isn't deemed done until all tests pass - `run_test` tool is used for this.
-   The document explains that for each feature the status needs to be updated when work is finished - `update_feature_status` tool is used for this.
-   The document explains that the task status needs to be updated when work is finished - `update_task_status` tool is used for this.
-   The document explains that if the work for the agent is done on a feature the `finish_feature` MUST BE USED.
-   The document explains that if the work for the agent is done on a task the `finish` MUST BE USED.
-   The document explains that if there's any unresolved issue - the `update_agent_question` tool is used for this.

## Tools

The Developer agent has access to the following tools:

### `get_context(files:[str])->[str]`
-   **Description**: Retrieves the content of specified files.

### `write_file(filename:str,content:str)`
-   **Description**: Writes or overwrites a file.

### `run_test(task_id:int,feature_id:str)->TestResult`
-   **Description**: Runs the test for a specific feature.

### `update_task_status(task_id:int,status:Status)->Task`
-   **Description**: Updates the status of a task.

### `update_feature_status(task_id:int,feature_id:str,status:Status)->Feature`
-   **Description**: Updates the status of a feature.

### `finish_feature(task_id:int,feature_id:str)->Feature`
-   **Description**: Marks a feature as complete.

### `finish(task_id:int)->Task`
-   **Description**: Marks a task as complete.

### `update_agent_question(task_id:int,feature_id:str?,question:str)`
-   **Description**: Poses a question to the user.
