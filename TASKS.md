# Tasks

See **[TASK_FORMAT.md](TASK_FORMAT.md)** for format reference and how to write acceptance criteria.

## Current Tasks

1) + Initial spec document
   Action: Create the founding SPEC.md document
   Acceptance: SPEC.md exists with WHAT, CORE IDEAS and ACTIONS sections
   Context: None

2) + Specification documentation
   Action: Analyse the specification format and what requirements it needs to provide.
   Acceptance: SPECIFICATION_GUIDE.md exists describing format, SPEC.md adheres to this format
   Context: SPEC.md

3) + First tasks
   Description: Create the initial task list for the project
   Acceptance: TASKS.md exists with at least 3 tasks and at least 1 pending task
   Context: SPEC.md

4) + Task format
   Action: Analyse the tasks and what requirements they need to provide. All the format and specification for that should be included in the documentation.
   Acceptance: TASK_FORMAT.md exists describing the format, TASKS.md adheres to this format
   Context: TASKS.md

5) + Specification template
   Action: Create a reusable template for writing new specifications
   Acceptance: TEMPLATE.md exists with all required sections from SPECIFICATION_GUIDE.md, with examples for each
   Context: SPECIFICATION_GUIDE.md
   Dependencies: 2

6) + Define Core Agent Terminology and Principles
   Action: Create the specification that defines the agent's high-level principles and establishes the key terms "Orchestrator" and "Agent".
   Acceptance: The file `AGENT_PRINCIPLES.md` exists and contains the required definitions.
   Context: SPEC.md

7) + Specify the Agent's Tool-Based Architecture
   Action: Create the complete technical specification for the agent's tool-based architecture. This task formally supersedes all previous, obsolete architecture documents.
   Acceptance:
    - The file `TOOL_ARCHITECTURE.md` exists and defines the JSON contract, the full suite of tools, and the safety/execution modes.
   Context: AGENT_PRINCIPLES.md

8) + Implement the Agent Orchestrator
   Action: Create the Python script that functions as the Agent's Orchestrator.
   Acceptance: The `scripts/run_local_agent.py` script is implemented and its functionality is fully compliant with the contracts and principles defined in `AGENT_PRINCIPLES.md` and `TOOL_ARCHITECTURE.md`.
   Context: AGENT_PRINCIPLES.md, TOOL_ARCHITECTURE.md
   Dependencies: 7

9) + Provide Orchestrator Dependencies
    Action: Create a dependency file that lists the external Python libraries required by the Orchestrator script.
    Acceptance: The file `requirements.txt` exists and contains all external libraries required to run `scripts/run_local_agent.py`.
    Context: scripts/run_local_agent.py
    Dependencies: 8

10) + Provide Orchestrator Configuration Template
    Action: Create a template for users to configure API keys for the Orchestrator.
    Acceptance: The file `.env.example` exists with placeholders for required API keys.
    Context: scripts/run_local_agent.py
    Dependencies: 8

11) + Create Final User Setup and Usage Guide
    Action: Write the comprehensive guide for setting up and running the agent.
    Acceptance: The file `LOCAL_SETUP.md` exists and provides clear, accurate instructions for the entire setup and execution process.
    Context: scripts/run_local_agent.py, requirements.txt, .env.example
    Dependencies: 8, 9, 10

12) + Plan specification
    Action: Create a plan specification that describes how each task should be executed.
    Acceptance: The file `PLAN_SPECIFICATION.md` exists and details the steps involved in creating a task plan.
    Context: SPECIFICATION_GUIDE.md, TASK_FORMAT.md

13) + Task plans
   Action: Create a plan for each task.
   Acceptance: A folder /plans with a plan file for each task exists.
   Context: PLAN_SPECIFICATION.md, TASKS.md
   Dependencies: 12

14) + File organisation specification
   Action: Create a scheme for organising files within the repository.
   Acceptance: The file `FILE_ORGANISATION.md` exists detailing the structure and naming conventions for different types of files and where they are stored
   Context: SPEC.md, TASKS.md

15) + Running local agent with context
   Action: Update `run_local_agent.py` so that it always has the base project context, that should be defined in a spec somewhere, as well as all files from a given task's `Context` field.
   Acceptance: `run_local_agent.py` includes the base project context and all files from a given task's `Context` field whenever running an agent.
   Context: TASKS.md, TASK_FORMAT.md, scripts/run_local_agent.py

16) - File organisation
   Action: Follow the scheme described in `FILE_ORGANISATION.md` to organise all files.
   Acceptance: All folders and files follow the conventions described in `FILE_ORGANISATION.md`.
   Context: FILE_ORGANISATION.md
   Notes: Perhaps new tools are necessary for this that allow renaming of files etc - this should be. This task and task 14 should probably exist much earlier in the hierarchy so that from the beginning the file organisation is correct. Also think about the organisation of this file (`TASKS.md`) so that it makes logical sense.
   Dependencies: 14

17) ? Feature definitions
   Action: Create a features specifications.
   Acceptance: The file `FEATURE_DEFINITIONS.md` exists detailing the features of the agent and how they will be implemented.
   Context: TASKS.md, TASK_FORMAT.md, FILE_ORGANISATION.md
   Notes: The purpose of this is to make task organisations better. Each task can be a set of sub-tasks, i.e. features, that each can have their own plan and can be run independently. A task is only complete once all of its features are complete. Until now it would be possible to achieve a similar effect by having multiple small tasks, but there's a very important thing that is lost here - the context for the whole overarching task. A feature might only need a very small context to be completed or it might need to know about the context of all of the other features to be completed well. A feature can have a nested sub-feature. This way a task will remain a very high level concept - detailing the absolute top level project goals, whereas a feature will focus more on details but still staying away from implementation specifics.
   Dependencies: 14

18) ? Running in isolation/container
   Action: Create a workflow to running the agent in a container, i.e. isolated environment.
   Acceptance: The file `RUNNING_IN_CONTAINER.md` exists detailing the steps involved in running the agent in a container environment.
   Context: scripts/run_local_agent.py
   Notes: The purpose is to have an agent periodically run in a container and not affect the host machine.

19) ? Running on cloud
   Action: Create a workflow to running the agent on cloud services such as AWS or Azure.
   Acceptance: The file `RUNNING_ON_CLOUD.md` exists detailing the steps involved in running the agent on cloud services.
   Context: RUNNING_IN_CONTAINER.md
   Dependencies: 16
   Notes: Once Task 16 is established, it should be possible to also host this project somewhere and have it perpetually run on a cloud service.

20) ? Run tests
   Action: Create a test framework for testing the agent's functionality.
   Acceptance: The file `TESTING.md` exists detailing the steps involved in testing the agent's functionality.
   Context: AGENT_PRINCIPLES.md, TOOL_ARCHITECTURE.md
   Notes: The test framework is implemented and can run tests on the agent - knowing the agent's output and the tools it can access, it needs to be able to determine if the agent has completed a task successfully or not.

21) ? Local app 
   Action: Create a local app to handle project management, see tasks etc.
   Acceptance: The file `LOCAL_APP.md` exists detailing the steps involved in creating a local
   Context: SPEC.md
   Notes: Currently I'm using VSCode to view the project, run everything, see tasks etc. It would be ideal to have a dedicated app for managing the project, viewing tasks, seeing progress etc. For being able to see how the agents fares etc. Cline the plugin for VSCode does something like this and maybe it makes sense to even built upon a fork on this. One thing to keep in mind is that we want to be really third-party independent. If we can create something ourselves we should. The only question is how it integrates with the project. If maintaining such a service/dependency is too heavy, then using a third party solution makes sense. Each third party solution should be its own tasks, with documented features and explanations as to why it was chosen etc.

22) ? Create a mobile app
    Action: Develop a mobile application that allows users to interact with the project and thus the agents it runs.
    Acceptance: The file `MOBILE_APP.md` exists detailing the development process and user interface design for the mobile application.
    Context: LOCAL_APP.md
    Notes: The purpose of this is to allow users to interact with the agent through a mobile device. It could include voice commands, touch gestures, or other input methods depending on the target audience and platform.
    Dependencies: 20

