# Tasks

See **[TASK_FORMAT.md](../docs/TASK_FORMAT.md)** for format reference and how to write acceptance criteria.

## Current Tasks

1) + Task format
   Action: Analyse the tasks and what requirements they need to provide. All the format and specification for that should be included in the documentation.
   Acceptance: `docs/TASK_FORMAT.md` exists describing the format, `tasks/TASKS.md` adheres to this format

2) + The spec
   Action: Create the founding `docs/SPEC.md` document
   Acceptance: `docs/SPEC.md` exists with WHAT, CORE IDEAS and ACTIONS sections

3) + File organisation specification
   Action: Create a scheme for organising files within the repository.
   Acceptance: The file `docs/FILE_ORGANISATION.md` exists detailing the structure and naming conventions for different types of files and where they are stored

4) + Specification documentation
   Action: Analyse the specification format and what requirements it needs to provide.
   Acceptance: `docs/SPECIFICATION_GUIDE.md` exists describing format, `docs/SPEC.md` adheres to this format
   Notes: A feature in this task should be to create a file `TEMPLATE.md` that has all the required sections from `docs/SPECIFICATION_GUIDE.md`, with examples for each section.

5) + Plan specification
    Action: Create a plan specification that describes how each task should be executed with information about creating features for tasks.
    Acceptance: The file `docs/PLAN_SPECIFICATION.md` exists and details the steps involved in creating a task plan. The file `docs/FEATURE_FORMAT.md` exists and details the format to use for features inside a plan.

6) + Define Core Agent Terminology and Principles
   Action: Create the specification that defines the agent's high-level principles and establishes the key terms "Orchestrator" and "Agent". The agent uses a tool-based architecture.
   Acceptance: The file `docs/AGENT_PRINCIPLES.md` exists and contains the required definitions. The file `docs/TOOL_ARCHITECTURE.md` exists and defines the JSON contract, the full suite of tools, and the execution modes.

7) - Agent Orchestrator
   Action: Create a script that functions as the Agent's Orchestrator - used for direct interaction with an LLM agent. 
   Notes: A script exists that allows interaction with an agent.

8) - Cleanup
   Action: Go over all specification documents and ensure that they adhere to their respective formats. The same goes for tasks and plans.

17) ? Running in isolation/container
   Action: Create a workflow to running the agent in a container, i.e. isolated environment.
   Acceptance: The file `docs/RUNNING_IN_CONTAINER.md` exists detailing the steps involved in running the agent in a container environment.
   Context: scripts/run_local_agent.py
   Notes: The purpose is to have an agent periodically run in a container and not affect the host machine.

18) ? Running on cloud
   Action: Create a workflow to running the agent on cloud services such as AWS or Azure.
   Acceptance: The file `docs/RUNNING_ON_CLOUD.md` exists detailing the steps involved in running the agent on cloud services.
   Context: docs/RUNNING_IN_CONTAINER.md
   Notes: Once containerization is established, it should be possible to also host this project somewhere and have it perpetually run on a cloud service.

19) ? Run tests
   Action: Create a test framework for testing the agent's functionality.
   Acceptance: The file `docs/TESTING.md` exists detailing the steps involved in testing the agent's functionality.
   Context: docs/AGENT_PRINCIPLES.md, docs/TOOL_ARCHITECTURE.md
   Notes: The test framework is implemented and can run tests on the agent - knowing the agent's output and the tools it can access, it needs to be able to determine if the agent has completed a task successfully or not.

20) ? Local app 
   Action: Create a local app to handle project management, see tasks etc.
   Acceptance: The file `docs/LOCAL_APP.md` exists detailing the steps involved in creating a local app for project management
   Context: docs/SPEC.md
   Notes: Currently I'm using VSCode to view the project, run everything, see tasks etc. It would be ideal to have a dedicated app for managing the project, viewing tasks, seeing progress etc. For being able to see how the agents fares etc. Cline the plugin for VSCode does something like this and maybe it makes sense to even built upon a fork on this. One thing to keep in mind is that we want to be really third-party independent. If we can create something ourselves we should. The only question is how it integrates with the project. If maintaining such a service/dependency is too heavy, then using a third party solution makes sense. Each third party solution should be its own tasks, with documented features and explanations as to why it was chosen etc.

21) ? Create a mobile app
    Action: Develop a mobile application that allows users to interact with the project and thus the agents it runs.
    Acceptance: The file `docs/MOBILE_APP.md` exists detailing the development process and user interface design for the mobile application.
    Context: docs/LOCAL_APP.md
    Notes: The purpose of this is to allow users to interact with the agent through a mobile device. It could include voice commands, touch gestures, or other input methods depending on the target audience and platform.
