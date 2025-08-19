# Tasks

See **[TASK_FORMAT.md](../docs/TASK_FORMAT.md)** for format reference and how to write acceptance criteria.

## Current Tasks

1) + Task format
   Action: Create documentation detailing the tasks' format.
   Acceptance: This document adheres to the format created and references it at the top.

2) - The spec
   Action: Create docs/SPEC.md as the single entry-point specification for the project.
   Acceptance:
     - `docs/SPECIFICATION_GUIDE.md` and `docs/TEMPLATE.md` exist.
     - `docs/SPEC.md` exists and adheres to `docs/SPECIFICATION_GUIDE.md`.

3) + File organisation specification
   Action: Create a scheme for organising files within the repository.
   Acceptance: 
   - `docs/FILE_ORGANISATION.md` exists.
   - The specification contains examples of how files should be organised.
   - All files are organised according to the specification.

4) + Plan specification
    Action: Create a plan specification that describes how each task should be executed with information about creating features for tasks.
    Acceptance: 
      - `docs/FEATURE_FORMAT.md` exists and includes Purpose, Format, Field Definitions, and Examples.
      - `docs/PLAN_SPECIFICATION.md` exists and includes purpose, principles, structure, template, and example, and references `docs/FEATURE_FORMAT.md`.

6) + Define Core Agent Terminology, Orchestrator, and Personas
   Action: Create the specification that defines the agent's high-level principles and establishes the key terms "Orchestrator" and "Agent". Consolidate the Orchestrator and Personas into a single cohesive agent architecture under this task.
   Acceptance: 
     - The documentation exists and is cohesive:
       - `docs/AGENT_PRINCIPLES.md` defines Agent vs Orchestrator and core principles and references the tools guide.
       - `docs/TOOL_ARCHITECTURE.md` defines the JSON contract, tools, and execution modes.
       - `docs/AGENT_PERSONAS.md` exists with four personas (Manager, Planner, Tester, Developer), each with responsibilities and clear prompts.
     - The Orchestrator lives at `scripts/run_local_agent.py` and supports persona mode with minimal-context prompts and the SAFE tools.
     - Plans/features from former task 7 are merged into `tasks/6/plan_6.md`; redundant files (if any) under `tasks/7`  are removed.
     - Tasks 7 and 10 are removed from `tasks/TASKS.md`.
     - Task 12 is marked `=` Deprecated as it is superseded by this merge.
   Rejection: all the features defining the code logic in task 7 are not present in task 6; `run_local_agent.py`, `run_persona.py`, `git_manager.py` and the whole `scripts` and especially `scripts\tools` folder is never mentioned ; folders for task 7 exist; The acceptance criteria for features is wrong;

8) + Tests specification
   Action: Create and maintain the canonical testing specification for the project and integrate testing requirements into the planning specification.
   Acceptance:
   - `docs/TESTING.md` exists and includes Required Sections: Purpose and Scope; Test Locations and Naming Conventions; Test Structure and Utilities; Writing Acceptance Tests; Running Tests; CI/Automation Expectations; Tool Usage; Examples; References.
   - `docs/PLAN_SPECIFICATION.md` is updated to include a "Test-Driven Acceptance" principle, references `docs/TESTING.md`, and updates its template and example to require a corresponding test per feature.
   - No feature should be simply a test run.

9) - Move tasks around
   Action: Perform the following:
   - Create a tool for moving a task to a different position in the list of tasks - the feature for it should be added to the plan for Task 7, the tests need to be created, and the code also.
   - The testing task - task 8, should be the moved to spot 5.
   - This task is completely removed.
   - All other tasks need to be shifted accordingly to be in order.

11) ? Should the tasks and plan format change?
   Action: Now that the personas exist, it's clear that to be able to provide them with the smallest context possible, we need to change the spec and thus the format of tasks and features. Instead of keeping a task in this markdown file, each task should be in a separate JSON file in its folder - `task.json`. The task should contain all the information that is currently here and all the feature specifics. This way it's easy to extract specific task or feature information and provide it as context to a given agent. The plan in each folder should remain as markdown, as it should be the best way for an LLM to consume information. Appropriate tools need to be in place, so that each persona will only get the relevant context.


13) - The plans for all tasks must be updated
   Action: Update the plans for all plans to reflect the status of each feature. Clearly there's something missing in the spec, most probably in `docs/PLAN_SPECIFICATION.md`, because the agent isn't updating the plan for the task it works on to update the status of the feature and task (while features are being worked on this should be set to pending).
   Acceptance: All tasks until this one have all plans updated with correct status, acceptance criteria and any other spec.

14) - New child projects structure
   Action: Create a new structure for child projects that stems from this project. This will be done by creating a new repository for each child project. Each child project is linked backed to this projct via git-submodules so that all the child projects are automatically updated whenever this project updates. This project drives the child projects and then the child projects can also be cloned independently if needed and will drive their own implementation work. This project will only oversee their specification correctness.
   Acceptance: The file `docs/CHILD_PROJECTS_SPECIFICATION.md` exists detailing the structure of child projects stemming from this project. There is a folder called `projects` where all the child projects are stored. Each child project has its own repository and is linked to this one via git submodules. This project's `.gitignore` needs to be updated so it ignores the `projects` folder and all the files inside it.

16) - Running in docker
   Action: Create a workflow to running the project in docker, i.e. isolated environment.
   Acceptance: The file `docs/docker/RUNNING_DOCKER_README.md` exists detailing the steps involved in running the project in a container environment. A `docs/docker/Dockerfile` exists that a user can copy and use. Ideally a script can exist that a use can us to clone the repository and build a docker image. At some point they will just have to provide the API keys, so maybe before the build docker script is is required that the user fills in a prepare `.env` file that the script will look into and set everything up.
   Remember, this is a regular task and requires a plan and features just like any other task.
   Notes: The purpose is to have an agent periodically run in a container and not affect the host machine.

17) ? First child project -> Libraries
   Action: Create a child project that focuses on libraries and tools for the agent. This includes creating reusable components, utilities, and frameworks that enhance the overall functionality and modularity of the agent system. The first things that should be included in there is the agent running code, the test running code, the git manager and all the tools an agent needs. Knowing how child projects work, it needs to make sense for the integration of this child project to work with other child projects.

18) - Local app 
   Action: Create a local Electron+React app to handle project management, see tasks etc.
   Acceptance: The project for the local app exists detailing the steps involved in creating a local app for project management. This will be the first project to stem from this one. It should follow the same exact principles as this project, but it will live in its own separate repository. This project is just meant to kickstart the whole scaffolding and specification. If any extra functionality comes into this project, it should be easy to adapt this Local app project to use the exact same ideas.
   Notes: Currently I'm using VSCode to view the project, run everything, see tasks etc. It would be ideal to have a dedicated app for managing the project, viewing tasks, seeing progress etc. For being able to see how the agents fares etc. Cline the plugin for VSCode does something like this and maybe it makes sense to even built upon a fork on this. One thing to keep in mind is that we want to be really third-party independent. If we can create something ourselves we should. The only question is how it integrates with the project. If maintaining such a service/dependency is too heavy, then using a third party solution makes sense. Each third party solution should be its own tasks, with documented features and explanations as to why it was chosen etc.

19) ? Create orchestration so that many different agents can be running on different tasks at once.
    Action: Implement orchestration logic to manage multiple agents simultaneously.
    Acceptance: The file `docs/ORCHESTration.md` exists detailing the implementation details and strategies for orchestrating multiple agents concurrently.
    Notes: This involves coordinating resources, scheduling tasks, monitoring performance, and ensuring seamless communication between agents. It may require distributed systems concepts and advanced programming techniques.
    Dependencies: 14

20) ? iOS app
    Action: Develop an iOS application that allows users to interact with the project and thus the agents it runs. Similarly to the Local app project - this is yet another project.
    Acceptance: The file `docs/MOBILE_APP.md` exists detailing the development process and user interface design for the mobile application.
    Notes: The purpose of this is to allow users to interact with the agent through a mobile device. It could include voice commands, touch gestures, or other input methods depending on the target audience and platform.

21) ? Backend
   Action: Create a way to easily launch a backend that all apps and agents can connect to. The backend must have a way to create a database that it can rely on.

22) ? Create a way to easily launch MCP servers
   Action: Our agents will need to access functionality that isn't local, it seems MCP servers are the current best way of doing so. Let's have a methodology/workflow to launch these easily.

23) - using LM Studio
   Action: Use LM Studio's server API to call different models. This is a local agent launch mode.

24) - explore other ways to launch agents locally
   Action: Explore alternative methods for launching agents locally, considering factors like scalability, efficiency, and ease of integration. This task aims to identify potential alternatives to the current approach and evaluate their suitability based on specific criteria.
   Acceptance: A comprehensive analysis report outlining the explored options, their pros and cons, and recommendations for future consideration.
