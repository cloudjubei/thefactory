# Tasks

See **[TASK_FORMAT.md](../docs/TASK_FORMAT.md)** for format reference and how to write acceptance criteria.

## Current Tasks

1) + Task format
   Action: Create documentation detailing the tasks' format.
   Acceptance: This document adheres to the format created and references it at the top.

2) + The spec
   Action: Create the spec that is the entry point for anyone to begin work on the project.
   Acceptance: The documentation exists.

3) + File organisation specification
   Action: Create a scheme for organising files within the repository.
   Acceptance: The documentation exists.

4) + Specification documentation
   Action: Analyse the specification format and what requirements it needs to provide.
   Acceptance: The documentation exists.
   Notes: A feature in this task should be to create a file `TEMPLATE.md` that has all the required sections from `docs/SPECIFICATION_GUIDE.md`, with examples for each section.

5) + Plan specification
    Action: Create a plan specification that describes how each task should be executed with information about creating features for tasks.
    Acceptance: The documentation exists.

6) + Tests specification
   Action: Create a test documentation for testing the agent's functionality for any task or feature.
   Acceptance: The documentation exists.

7) + Define Core Agent Terminology and Principles
   Action: Create the specification that defines the agent's high-level principles and establishes the key terms "Orchestrator" and "Agent". The agent uses a tool-based architecture.
   Acceptance: The documentation exists.

8) - Agent Orchestrator
   Action: Create a script that functions as the Agent's Orchestrator - used for direct interaction with an LLM agent.
   Acceptance: A script exists that allows interaction with an agent. Step 1, the agent determines the task to work in response it is told whether a plan for that task exists and is given it if it does. Before the response, the agent is switched to the correct feature branch for that task. Step 2, the agent determines the minimal context it requires to work on the task it chose in response it receives the context files. Step 3 - the agent works on the task until completion.

9) - Automated tests
   Action: Create tests for every task and feature already existing. 
   Acceptance: Automated tests pass for all tasks and features. All plans for tasks have information about writing tests included in their action steps. All features have a corresponding test file and this is described as a mandatory step in `docs/PLAN_SPECIFICATION.md`. A feature is only ever completely done when there is a test written for it and it passed. This should also be described in the plan specification.
   Notes: These are unit tests that check the agent's ability to perform specific tasks and features. They should cover various scenarios and edge cases to ensure robustness and reliability.

10) + Move tests spec
   Action: The test spec task should be right after the plan specification "task 5". Move everything around correctly so that they're in order, as that will maintain a cohesive chronological order.
   Acceptance: The test specification task is "task 6" and the other tasks that were after "task 5" are shifted.

11) - Running in isolation/container
   Action: Create a workflow to running the agent in a container, i.e. isolated environment.
   Acceptance: The file `docs/RUNNING_IN_CONTAINER.md` exists detailing the steps involved in running the agent in a container environment.
   Notes: The purpose is to have an agent periodically run in a container and not affect the host machine.

12) - Running on cloud
   Action: Create a workflow to running the agent on cloud services such as AWS or Azure.
   Acceptance: The file `docs/RUNNING_ON_CLOUD.md` exists detailing the steps involved in running the agent on cloud services.
   Notes: Once containerization is established, it should be possible to also host this project somewhere and have it perpetually run on a cloud service.


13) ? Local app 
   Action: Create a local app to handle project management, see tasks etc.
   Acceptance: The file `docs/LOCAL_APP.md` exists detailing the steps involved in creating a local app for project management
   Notes: Currently I'm using VSCode to view the project, run everything, see tasks etc. It would be ideal to have a dedicated app for managing the project, viewing tasks, seeing progress etc. For being able to see how the agents fares etc. Cline the plugin for VSCode does something like this and maybe it makes sense to even built upon a fork on this. One thing to keep in mind is that we want to be really third-party independent. If we can create something ourselves we should. The only question is how it integrates with the project. If maintaining such a service/dependency is too heavy, then using a third party solution makes sense. Each third party solution should be its own tasks, with documented features and explanations as to why it was chosen etc.

14) ? Create a mobile app
    Action: Develop a mobile application that allows users to interact with the project and thus the agents it runs.
    Acceptance: The file `docs/MOBILE_APP.md` exists detailing the development process and user interface design for the mobile application.
    Notes: The purpose of this is to allow users to interact with the agent through a mobile device. It could include voice commands, touch gestures, or other input methods depending on the target audience and platform.

15) ? Create orchestration so that many different agents can be running on different tasks at once.
    Action: Implement orchestration logic to manage multiple agents simultaneously.
    Acceptance: The file `docs/ORCHESTRATION.md` exists detailing the implementation details and strategies for orchestrating multiple agents concurrently.
    Notes: This involves coordinating resources, scheduling tasks, monitoring performance, and ensuring seamless communication between agents. It may require distributed systems concepts and advanced programming techniques.
