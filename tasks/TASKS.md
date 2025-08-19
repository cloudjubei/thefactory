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

6) + Agent Principles and Orchestrator
   Action: Define the agent's high-level principles and establish the key terms "Orchestrator" and "Agent", and implement the Orchestrator script used for direct interaction with an LLM agent.
   Acceptance: The documentation exists and a script exists that allows interaction with an agent.

8) + Tests specification
   Action: Create a test documentation for testing the agent's functionality for any task or feature.
   Acceptance: The documentation exists.

9) - Automated tests
   Action: Create tests for every task and feature already existing. 
   Acceptance: Automated tests pass for all tasks and features. All plans for tasks have information about writing tests included in their action steps. All features have a corresponding test file and this is described as a mandatory step in `docs/PLAN_SPECIFICATION.md`. A feature is only ever completely done when there is a test written for it and it passed. This should also be described in the plan specification. The tests for this task must all pass.

11) - The plans for all tasks must be updated
   Action: Update the plans for all plans to reflect the status of each feature. Clearly there's something missing in the spec, most probably in `docs/PLAN_SPECIFICATION.md`, because the agent isn't updating the plan for the task it works on to update the status of the feature and task (while features are being worked on this should be set to pending).
   Acceptance: All tasks until this one have all plans updated with correct status, acceptance criteria and any other spec.

12) - New child projects structure
   Action: Create a new structure for child projects that stems from this project. This will be done by creating a new repository for each child project. Each child project is linked backed to this projct via git-submodules so that all the child projects are automatically updated whenever this project updates. This project drives the child projects and then the child projects can also be cloned independently if needed and will drive their own implementation work. This project will only oversee their specification correctness.
   Acceptance: The file `docs/CHILD_PROJECTS_SPECIFICATION.md` exists detailing the structure of child projects stemming from this project. There is a folder called `projects` where all the child projects are stored. Each child project has its own repository and is linked to this one via git submodules. This project's `.gitignore` needs to be updated so it ignores the `projects` folder and all the files inside it.

13) - Move tests spec
   Action: Perform the following:
   - Merge task 9 with task 8, leaving only task 8. 
   - The updated task 8, should be right after the plan specification "task 5". Move everything around correctly so that they're in order, as that will maintain a cohesive chronological order.
   Acceptance: The general "testing" task is "task 6" and the other tasks that were after "task 5" are shifted. This means all the plans and dependent files of all tasks involved have moved as well.

14) - Running in docker
   Action: Create a workflow to running the project in docker, i.e. isolated environment.
   Acceptance: The file `docs/docker/RUNNING_DOCKER_README.md` exists detailing the steps involved in running the project in a container environment. A `docs/docker/Dockerfile` exists that a user can copy and use. Ideally a script can exist that a use can us to clone the repository and build a docker image. At some point they will just have to provide the API keys, so maybe before the build docker script is is required that the user fills in the API keys in a prepare `.env` file that the script will look into and set everything up.
   Remember, this is a regular task and requires a plan and features just like any other task.
   Notes: The purpose is to have an agent periodically run in a container and not affect the host machine.

15) ? First child project -> Libraries
   Action: Create a child project that focuses on libraries and tools for the agent. This includes creating reusable components, utilities, and frameworks that enhance the overall functionality and modularity of the agent system. The first things that should be included in there is the agent running code, the test running code, the git manager and all the tools an agent needs. Knowing how child projects work, it needs to make sense for the integration of this child project to work with other child projects.

17) - Local app 
   Action: Create a local Electron+React app to handle project management, see tasks etc.
   Acceptance: The project for the local app exists detailing the steps involved in creating a local app for project management. This will be the first project to stem from this one. It should follow the same exact principles as this project, but it will live in its own separate repository. This project is just meant to kickstart the whole scaffolding and specification. If any extra functionality comes into this project, it should be easy to adapt this Local app project to use the exact same ideas.
   Notes: Currently I'm using VSCode to view the project, run everything, see tasks etc. It would be ideal to have a dedicated app for managing the project, viewing tasks, seeing progress etc. For being able to see how the agents fares etc. Cline the plugin for VSCode does something like this and maybe it makes sense to even built upon a fork on this. One thing to keep in mind is that we want to be really third-party independent. If we can create something ourselves we should. The only question is how it integrates with the project. If maintaining such a service/dependency is too heavy, then using a third party solution makes sense. Each third party solution should be its own tasks, with documented features and explanations as to why it was chosen etc.

14) ? Create orchestration so that many different agents can be running on different tasks at once.
    Action: Implement orchestration logic to manage multiple agents simultaneously.
    Acceptance: The file `docs/ORCHESTration.md` exists detailing the implementation details and strategies for orchestrating multiple agents concurrently.
    Notes: This involves coordinating resources, scheduling tasks, monitoring performance, and ensuring seamless communication between agents. It may require distributed systems concepts and advanced programming techniques.
    Dependencies: 13

15) ? iOS app
    Action: Develop an iOS application that allows users to interact with the project and thus the agents it runs. Similarly to the Local app project - this is yet another project.
    Acceptance: The file `docs/MOBILE_APP.md` exists detailing the development process and user interface design for the mobile application.
    Notes: The purpose of this is to allow users to interact with the agent through a mobile device. It could include voice commands, touch gestures, or other input methods depending on the target audience and platform.

16) ? Backend
   Action: Create a way to easily launch a backend that all apps and agents can connect to. The backend must have a way to create a database that it can rely on.

17) ? Create a way to easily launch MCP servers
   Action: Our agents will need to access functionality that isn't local, it seems MCP servers are the current best way of doing so. Let's have a methodology/workflow to launch these easily.

18) - using LM Studio
   Action: Use LM Studio's server API to call different models. This is a local agent launch mode.

19) - explore other ways to launch agents locally
   Action: Explore alternative methods for launching agents locally, considering factors like scalability, efficiency, and ease of integration. This task aims to identify potential alternatives to the current approach and evaluate their suitability based on specific criteria.
   Acceptance: A comprehensive analysis report outlining the explored options, their pros and cons, and recommendations for future consideration.
