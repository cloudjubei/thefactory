# Tasks

See **[TASK_FORMAT.md](../docs/TASK_FORMAT.md)** for format reference and how to write acceptance criteria.

## Current Tasks

1) + Initial spec document
   Action: Create the founding `docs/SPEC.md` document
   Acceptance: `docs/SPEC.md` exists with WHAT, CORE IDEAS and ACTIONS sections
   Context: None

2) + Specification documentation
   Action: Analyse the specification format and what requirements it needs to provide.
   Acceptance: `docs/SPECIFICATION_GUIDE.md` exists describing format, `docs/SPEC.md` adheres to this format
   Context: docs/SPEC.md

3) + Task format
   Action: Analyse the tasks and what requirements they need to provide. All the format and specification for that should be included in the documentation.
   Acceptance: `docs/TASK_FORMAT.md` exists describing the format, `docs/TASKS.md` adheres to this format
   Context: docs/SPEC.md

4) + Specification template
   Action: Create a reusable template for writing new specifications
   Acceptance: `TEMPLATE.md` exists with all required sections from `docs/SPECIFICATION_GUIDE.md`, with examples for each
   Context: docs/SPECIFICATION_GUIDE.md

5) + Define Core Agent Terminology and Principles
   Action: Create the specification that defines the agent's high-level principles and establishes the key terms "Orchestrator" and "Agent".
   Acceptance: The file `docs/AGENT_PRINCIPLES.md` exists and contains the required definitions.
   Context: docs/SPEC.md

6) + Specify the Agent's Tool-Based Architecture
   Action: Create the complete technical specification for the agent's tool-based architecture.
   Acceptance: The file `docs/TOOL_ARCHITECTURE.md` exists and defines the JSON contract, the full suite of tools, and the safety/execution modes.
   Context: docs/AGENT_PRINCIPLES.md

7) + Implement the Agent Orchestrator
   Action: Create the Python script that functions as the Agent's Orchestrator.
   Acceptance: The `scripts/run_local_agent.py` script is implemented and its functionality is fully compliant with the contracts and principles defined in `docs/AGENT_PRINCIPLES.md` and `docs/TOOL_ARCHITECTURE.md`.
   Context: docs/AGENT_PRINCIPLES.md, docs/TOOL_ARCHITECTURE.md

8) + Provide Orchestrator Dependencies
    Action: Create a dependency file that lists the external Python libraries required by the Orchestrator script.
    Acceptance: The file `requirements.txt` exists and contains all external libraries required to run `scripts/run_local_agent.py`.
    Context: scripts/run_local_agent.py

9) + Provide Orchestrator Configuration Template
    Action: Create a template for users to configure API keys for the Orchestrator.
    Acceptance: The file `.env.example` exists with placeholders for required API keys.
    Context: scripts/run_local_agent.py

10) + Create Final User Setup and Usage Guide
    Action: Write the comprehensive guide for setting up and running the agent.
    Acceptance: The file `docs/LOCAL_SETUP.md` exists and provides clear, accurate instructions for the entire setup and execution process.
    Context: scripts/run_local_agent.py, requirements.txt, .env.example

11) + Plan specification
    Action: Create a plan specification that describes how each task should be executed.
    Acceptance: The file `docs/PLAN_SPECIFICATION.md` exists and details the steps involved in creating a task plan.
    Context: docs/SPECIFICATION_GUIDE.md, docs/TASK_FORMAT.md

12) + File organisation specification
   Action: Create a scheme for organising files within the repository.
   Acceptance: The file `docs/FILE_ORGANISATION.md` exists detailing the structure and naming conventions for different types of files and where they are stored
   Context: docs/SPEC.md, tasks/TASKS.md

13) + Tasks, Plans and Features
   Action: Update `tasks/TASKS.md`, `docs/TASK_FORMAT.md`, `docs/PLAN_SPECIFICATION.md`, `docs/FEATURE_FORMAT.md`, `docs/SPEC.md`, `docs/FILE_ORGANISATION.md`.
   Acceptance: The agent always when taking on a task creates a `plan_{id}.md` inside `tasks\{id}` folder. The plan holds details about all the features that make up the task. `TASKS.md` stays high level and `TASK_FORMAT.md` is also updated if any changes occur. `FEATURE_FORMAT.md` is updated to include any relevant information. `PLAN_SPECIFICATION.md` is updated to highlight what an agent must do to proceed with any task. An agent's path is the following: read `SPEC.md`, then (because it's an action inside) read `PLAN_SPCIFICATION.md`, and then the next action is to take on a task from `TASKS.md`. The file `FILE_ORGANISATION.md` is updated to hold the information about tasks and plans.
   Context: `tasks/TASKS.md`, `docs/TASK_FORMAT.md`, `docs/PLAN_SPECIFICATION.md`, `docs/FEATURE_FORMAT.md`, `docs/SPEC.md`, `docs/FILE_ORGANISATION.md`

15) - Running specific tasks and features
   Action: `scripts/run_local_agent.py` is run with the optional argument `-t {task_id}` and `-f {feature_id}` (only if task_id is given). This will cause the agent to execute the specified task and the given feature.
   Acceptance: The agent executes the specified task or a feature in a task and outputs the result. The agent must create a branch for this that follows the convention `features/{task_id}_{feature_id}` or `tasks/{task_id}` if no feature is specified.
   Context: scripts/run_local_agent.py, tasks/TASKS.md

16) - Cleanup
   Action: Ensure that everything follows all current specifications. Look at all the files provided in the context, the current tasks, features and plans. Ensure that there are no inconsistencies between the files and that the files are up to date. An agent must know that at any point during task & feature work, they are able to update/rewrite the spec docs in case there is a change that requires such an update. This is especially relevant if during work on a feature, the plan should change and perhaps new features should be added to the task.
   Context: docs/SPEC.md, docs/TASK_FORMAT.md, docs/FILE_ORGANISATION.md, docs/FEATURE_FORMAT.md, tasks/TASKS.md, docs/PLAN_SPECIFICATION.md, docs/AGENT_PRINCIPLES.md, plans/, scripts/run_local_agent.py, requirements.txt, .env.example, LOCAL_SETUP.md

17) ? Running in isolation/container
   Action: Create a workflow to running the agent in a container, i.e. isolated environment.
   Acceptance: The file `RUNNING_IN_CONTAINER.md` exists detailing the steps involved in running the agent in a container environment.
   Context: scripts/run_local_agent.py
   Notes: The purpose is to have an agent periodically run in a container and not affect the host machine.

18) ? Running on cloud
   Action: Create a workflow to running the agent on cloud services such as AWS or Azure.
   Acceptance: The file `RUNNING_ON_CLOUD.md` exists detailing the steps involved in running the agent on cloud services.
   Context: docs/RUNNING_IN_CONTAINER.md
   Notes: Once containerization is established, it should be possible to also host this project somewhere and have it perpetually run on a cloud service.

19) ? Run tests
   Action: Create a test framework for testing the agent's functionality.
   Acceptance: The file `TESTING.md` exists detailing the steps involved in testing the agent's functionality.
   Context: docs/AGENT_PRINCIPLES.md, docs/TOOL_ARCHITECTURE.md
   Notes: The test framework is implemented and can run tests on the agent - knowing the agent's output and the tools it can access, it needs to be able to determine if the agent has completed a task successfully or not.

20) ? Local app 
   Action: Create a local app to handle project management, see tasks etc.
   Acceptance: The file `LOCAL_APP.md` exists detailing the steps involved in creating a local app for project management
   Context: docs/SPEC.md
   Notes: Currently I'm using VSCode to view the project, run everything, see tasks etc. It would be ideal to have a dedicated app for managing the project, viewing tasks, seeing progress etc. For being able to see how the agents fares etc. Cline the plugin for VSCode does something like this and maybe it makes sense to even built upon a fork on this. One thing to keep in mind is that we want to be really third-party independent. If we can create something ourselves we should. The only question is how it integrates with the project. If maintaining such a service/dependency is too heavy, then using a third party solution makes sense. Each third party solution should be its own tasks, with documented features and explanations as to why it was chosen etc.

21) ? Create a mobile app
    Action: Develop a mobile application that allows users to interact with the project and thus the agents it runs.
    Acceptance: The file `MOBILE_APP.md` exists detailing the development process and user interface design for the mobile application.
    Context: docs/LOCAL_APP.md
    Notes: The purpose of this is to allow users to interact with the agent through a mobile device. It could include voice commands, touch gestures, or other input methods depending on the target audience and platform.
