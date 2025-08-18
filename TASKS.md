# Tasks

See **[TASK_FORMAT.md](TASK_FORMAT.md)** for format reference and how to write acceptance criteria.

## Current Tasks

1) + Initial spec document
   Action: Create the founding SPEC.md document
   Acceptance: SPEC.md exists with WHAT, CORE IDEAS and ACTIONS sections

2) + Specification documentation
   Action: Analyse the specification format and what requirements it needs to provide.
   Acceptance: SPECIFICATION_GUIDE.md exists describing format, SPEC.md adheres to this format

3) + First tasks
   Description: Create the initial task list for the project
   Acceptance: TASKS.md exists with at least 3 tasks and at least 1 pending task

4) + Task format
   Action: Analyse the tasks and what requirements they need to provide. All the format and specification for that should be included in the documentation.
   Acceptance: TASK_FORMAT.md exists describing the format, TASKS.md adheres to this format

5) + Specification template
   Action: Create a reusable template for writing new specifications
   Acceptance: TEMPLATE.md exists with all required sections from SPECIFICATION_GUIDE.md, with examples for each
   Dependencies: 2

6) + Define Core Agent Terminology and Principles
   Action: Create the specification that defines the agent's high-level principles and establishes the key terms "Orchestrator" and "Agent".
   Acceptance: The file `AGENT_PRINCIPLES.md` exists and contains the required definitions.

7) + Specify the Agent's Tool-Based Architecture
   Action: Create the complete technical specification for the agent's tool-based architecture. This task formally supersedes all previous, obsolete architecture documents.
   Acceptance:
    - The file `TOOL_ARCHITECTURE.md` exists and defines the JSON contract, the full suite of tools, and the safety/execution modes.

8) + Implement the Agent Orchestrator
   Action: Create the Python script that functions as the Agent's Orchestrator.
   Acceptance: The `scripts/run_local_agent.py` script is implemented and its functionality is fully compliant with the contracts and principles defined in `AGENT_PRINCIPLES.md` and `TOOL_ARCHITECTURE.md`.
   Dependencies: 7

9) + Provide Orchestrator Dependencies
    Action: Create a dependency file that lists the external Python libraries required by the Orchestrator script.
    Acceptance: The file `requirements.txt` exists and contains all external libraries required to run `scripts/run_local_agent.py`.
    Dependencies: 8

10) + Provide Orchestrator Configuration Template
    Action: Create a template for users to configure API keys for the Orchestrator.
    Acceptance: The file `.env.example` exists with placeholders for required API keys.
    Dependencies: 8

11) + Create Final User Setup and Usage Guide
    Action: Write the comprehensive guide for setting up and running the agent.
    Acceptance: The file `LOCAL_SETUP.md` exists and provides clear, accurate instructions for the entire setup and execution process.
    Dependencies: 8, 9, 10

12) + Plan specification
    Action: Create a plan specification that describes how each task should be executed.
    Acceptance: The file `PLAN_SPECIFICATION.md` exists and details the steps involved in creating a task plan.

13) + Task plans
   Action: Create a plan for each task.
   Acceptance: A folder /plans with a plan file for each task exists.
   Dependencies: 12

14) + File organisation
   Action: Create a scheme for organising files within the repository.
   Acceptance: The file `FILE_ORGANISATION.md` exists detailing the structure and naming conventions for different types of files and where they are stored.

15) ? Tackle growth
   Action: Create a system for representing tasks and their plans.
   Acceptance: A folder /tasks with a task file for each task exists.
   Dependencies: 13
   Notes: The project is growing and there's a definite need to organise things better than just having everything in one place. Maybe a special DSL is required, or a different scheme to more succinctly describe thing. This file is great for now, but once there are 1000s of tasks, we'll need something else - we need to prepare for that.

16) ? Running in isolation/container
   Action: Create a workflow to running the agent in a container, i.e. isolated environment.
   Acceptance: The file `RUNNING_IN_CONTAINER.md` exists detailing the steps involved in running the agent in a container environment.
   Notes: The purpose is to have an agent periodically run in a container and not affect the host machine.

17) ? Running on cloud
   Action: Create a workflow to running the agent on cloud services such as AWS or Azure.
   Acceptance: The file `RUNNING_ON_CLOUD.md` exists detailing the steps involved in running the agent on cloud services.
   Dependencies: 16
   Notes: Once Task 16 is established, it should be possible to also host this project somewhere and have it perpetually run on a cloud service.

18) ? Run tests
   Action: Create a test framework for testing the agent's functionality.
   Acceptance: The file `TESTING.md` exists detailing the steps involved in testing the agent's functionality.
   Notes: The test framework is implemented and can run tests on the agent - knowing the agent's output and the tools it can access, it needs to be able to determine if the agent has completed a task successfully or not.

19) ? Feature definitions
   Action: Create a features specifications.
   Acceptance: The file `FEATURE_DEFINITIONS.md` exists detailing the features of the agent and how they will be implemented.
   Notes: The purpose of this is to make task organisations better. Each task can be a set of sub-tasks, i.e. features, that each can have their own plan and can be run independently. A task is only complete once all of its features are complete. Until now it would be possible to achieve a similar effect by having multiple small tasks, but there's a very important thing that is lost here - the context for the whole overarching task. A feature might only need a very small context to be completed or it might need to know about the context of all of the other features to be completed well. A feature can have a nested sub-feature. This way a task will remain a very high level concept - detailing the absolute top level project goals, whereas a feature will focus more on details but still staying away from implementation specifics.
