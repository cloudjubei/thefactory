# Tasks

See **[TASK_FORMAT.md](../docs/TASK_FORMAT.md)** for format reference and how to write acceptance criteria.

## Current Tasks

1) + Initial spec document
   Action: Create the founding SPEC.md document
   Acceptance: SPEC.md exists with WHAT, CORE IDEAS and ACTIONS sections
   Context: None

   Features:
     Feature 1) + Draft SPEC structure
        Action: Create WHAT, CORE IDEAS, and ACTIONS sections in SPEC.md.
        Acceptance: SPEC.md includes all three sections with meaningful content.
        Context: docs/SPECIFICATION_GUIDE.md

     Feature 2) + Align with spec philosophy
        Action: Ensure SPEC.md focuses on WHAT, not HOW.
        Acceptance: SPEC.md avoids implementation details.
        Context: docs/SPECIFICATION_GUIDE.md

2) + Specification documentation
   Action: Analyse the specification format and what requirements it needs to provide.
   Acceptance: SPECIFICATION_GUIDE.md exists describing format, SPEC.md adheres to this format
   Context: docs/SPEC.md

   Features:
     Feature 1) + Define core components
        Action: Provide Problem, Inputs/Outputs, Constraints, Success Criteria, Edge Cases.
        Acceptance: Sections present and clearly defined.
        Context: docs/SPECIFICATION_GUIDE.md

     Feature 2) + Provide good vs bad example
        Action: Include both examples to illustrate quality.
        Acceptance: Examples exist and are consistent.
        Context: docs/SPECIFICATION_GUIDE.md

     Feature 3) + Define Self-Cleaning Principle
        Action: Document how specs replace obsolete paradigms.
        Acceptance: Principle is clearly articulated.
        Context: docs/SPECIFICATION_GUIDE.md

3) + Task format
   Action: Analyse the tasks and what requirements they need to provide. All the format and specification for that should be included in the documentation.
   Acceptance: TASK_FORMAT.md exists describing the format, TASKS.md adheres to this format
   Context: docs/SPEC.md

   Features:
     Feature 1) + Define task fields and statuses
        Action: Document field definitions and status codes.
        Acceptance: TASK_FORMAT.md contains complete definitions.
        Context: docs/TASK_FORMAT.md

     Feature 2) + Provide examples
        Action: Include simple and complex examples.
        Acceptance: Examples are present and readable.
        Context: docs/TASK_FORMAT.md

     Feature 3) + Introduce feature section in tasks
        Action: Extend format to support Features under Tasks.
        Acceptance: TASK_FORMAT.md includes Features section with numbering and rules.
        Context: docs/FEATURES_SPECIFICATION.md, docs/TASK_FORMAT.md

4) + Specification template
   Action: Create a reusable template for writing new specifications
   Acceptance: TEMPLATE.md exists with all required sections from SPECIFICATION_GUIDE.md, with examples for each
   Context: docs/SPECIFICATION_GUIDE.md

   Features:
     Feature 1) + Create template with placeholders
        Action: Include all sections with example placeholders.
        Acceptance: TEMPLATE.md contains complete skeleton.
        Context: docs/SPECIFICATION_GUIDE.md

5) + Define Core Agent Terminology and Principles
   Action: Create the specification that defines the agent's high-level principles and establishes the key terms "Orchestrator" and "Agent".
   Acceptance: The file `AGENT_PRINCIPLES.md` exists and contains the required definitions.
   Context: docs/SPEC.md

   Features:
     Feature 1) + Define terminology
        Action: Define Agent and Orchestrator roles.
        Acceptance: Both terms defined in AGENT_PRINCIPLES.md.
        Context: docs/AGENT_PRINCIPLES.md

     Feature 2) + Document core principles
        Action: Capture specification-driven, LLM-led, and interaction principles.
        Acceptance: Principles section present and accurate.
        Context: docs/AGENT_PRINCIPLES.md

6) + Specify the Agent's Tool-Based Architecture
   Action: Create the complete technical specification for the agent's tool-based architecture.
   Acceptance: The file `TOOL_ARCHITECTURE.md` exists and defines the JSON contract, the full suite of tools, and the safety/execution modes.
   Context: docs/AGENT_PRINCIPLES.md

   Features:
     Feature 1) + Define JSON response contract
        Action: Specify plan + tool_calls structure and schema.
        Acceptance: Schema present and precise.
        Context: docs/TOOL_ARCHITECTURE.md

     Feature 2) + Enumerate tools and arguments
        Action: List and define all available tools.
        Acceptance: All tools documented with arguments and behavior.
        Context: docs/TOOL_ARCHITECTURE.md

     Feature 3) + Execution modes and workflow
        Action: Define single/continuous modes and mandatory workflow.
        Acceptance: Modes and workflow described.
        Context: docs/TOOL_ARCHITECTURE.md

7) + Implement the Agent Orchestrator
   Action: Create the Python script that functions as the Agent's Orchestrator.
   Acceptance: The `scripts/run_local_agent.py` script is implemented and its functionality is fully compliant with the contracts and principles defined in `AGENT_PRINCIPLES.md` and `TOOL_ARCHITECTURE.md`.
   Context: docs/AGENT_PRINCIPLES.md, docs/TOOL_ARCHITECTURE.md

   Features:
     Feature 1) + Prompt and plan handling
        Action: Build prompts with context and request JSON plan/tool_calls.
        Acceptance: UnifiedEngine constructs messages and parses JSON.
        Context: scripts/run_local_agent.py

     Feature 2) + Tool execution layer
        Action: Implement AgentTools for safe file ops, renames, submission, Q/A, finish.
        Acceptance: Methods map 1:1 with specs.
        Context: scripts/run_local_agent.py, docs/TOOL_ARCHITECTURE.md

     Feature 3) + Context gathering
        Action: Provide consistent set of context files to the Agent.
        Acceptance: _gather_context includes core docs and scripts as listed.
        Context: scripts/run_local_agent.py

     Feature 4) + CLI and modes
        Action: Support single and continuous execution modes.
        Acceptance: CLI flags work; modes behave per spec.
        Context: scripts/run_local_agent.py, docs/TOOL_ARCHITECTURE.md

8) + Provide Orchestrator Dependencies
    Action: Create a dependency file that lists the external Python libraries required by the Orchestrator script.
    Acceptance: The file `requirements.txt` exists and contains all external libraries required to run `scripts/run_local_agent.py`.
    Context: scripts/run_local_agent.py

   Features:
     Feature 1) + Identify dependencies
        Action: Determine required libraries (e.g., python-dotenv, LiteLLM, git tools).
        Acceptance: requirements.txt contains necessary packages.
        Context: scripts/run_local_agent.py

9) + Provide Orchestrator Configuration Template
    Action: Create a template for users to configure API keys for the Orchestrator.
    Acceptance: The file `.env.example` exists with placeholders for required API keys.
    Context: scripts/run_local_agent.py

   Features:
     Feature 1) + Define env variables
        Action: List required variables and defaults/placeholders.
        Acceptance: .env.example includes all necessary keys.
        Context: scripts/run_local_agent.py

10) + Create Final User Setup and Usage Guide
    Action: Write the comprehensive guide for setting up and running the agent.
    Acceptance: The file `LOCAL_SETUP.md` exists and provides clear, accurate instructions for the entire setup and execution process.
    Context: scripts/run_local_agent.py, requirements.txt, .env.example

   Features:
     Feature 1) + Setup instructions
        Action: Document environment setup and installation.
        Acceptance: Steps are complete and reproducible.
        Context: LOCAL_SETUP.md

     Feature 2) + Usage and troubleshooting
        Action: Document how to run the agent and common issues.
        Acceptance: Guide includes examples and troubleshooting tips.
        Context: LOCAL_SETUP.md

11) + Plan specification
    Action: Create a plan specification that describes how each task should be executed.
    Acceptance: The file `PLAN_SPECIFICATION.md` exists and details the steps involved in creating a task plan.
    Context: docs/SPECIFICATION_GUIDE.md, docs/TASK_FORMAT.md

   Features:
     Feature 1) + Define plan principles
        Action: Specify purpose, atomicity, logical sequence, clarity.
        Acceptance: PLAN_SPECIFICATION.md includes these sections.
        Context: docs/PLAN_SPECIFICATION.md

     Feature 2) + Provide example mapping to tool calls
        Action: Show example plan mapping to required workflow.
        Acceptance: Example present and accurate.
        Context: docs/PLAN_SPECIFICATION.md

12) + File organisation specification
   Action: Create a scheme for organising files within the repository.
   Acceptance: The file `FILE_ORGANISATION.md` exists detailing the structure and naming conventions for different types of files and where they are stored
   Context: docs/SPEC.md, tasks/TASKS.md

   Features:
     Feature 1) + Define directory structure
        Action: Provide a clear, scalable top-level layout.
        Acceptance: Structure is documented with rationale.
        Context: docs/FILE_ORGANISATION.md

     Feature 2) + Naming conventions
        Action: Establish naming conventions for docs/scripts/config.
        Acceptance: Conventions are listed and justified.
        Context: docs/FILE_ORGANISATION.md

13) + Feature specification
   Action: Create a features specification.
   Acceptance: The file `FEATURES_SPECIFICATION.md` exists detailing the features of the agent and how they will be implemented. A feature should be defined as closely to a task as possible - i.e. following the same format. `docs/FILE_ORGANISATION.md` is updated to reflect these new files, where they exist and how they are referenced. `docs/TASK_FORMAT.md` is updated to reflect that tasks have features. `tasks/TASKS.md` is updated to now have a set of features for each task.
   Context: tasks/TASKS.md, docs/TASK_FORMAT.md, docs/FILE_ORGANISATION.md
   Notes: The purpose of this is to make task organisations better. Each task can be a set of sub-tasks, i.e. features, that each can have their own plan and can be run independently. A task is only complete once all of its features are complete. Until now it would be possible to achieve a similar effect by having multiple small tasks, but there's a very important thing that is lost here - the context for the whole overarching task. A feature might only need a very small context to be completed or it might need to know about the context of all of the other features to be completed well. A feature can have a nested sub-feature. This way a task will remain a very high level concept - detailing the absolute top level project goals, whereas a feature will focus more on details but still staying away from implementation specifics.

   Features:
     Feature 1) + Create FEATURES_SPECIFICATION.md
        Action: Define feature concept, format, lifecycle, and agent feature catalog.
        Acceptance: docs/FEATURES_SPECIFICATION.md exists with the above.
        Context: docs/FEATURES_SPECIFICATION.md, docs/SPECIFICATION_GUIDE.md

     Feature 2) + Update TASK_FORMAT.md to include Features
        Action: Extend TASK_FORMAT.md with a Features section and example.
        Acceptance: TASK_FORMAT.md shows feature fields and numbering.
        Context: docs/TASK_FORMAT.md

     Feature 3) + Update FILE_ORGANISATION.md to reference features
        Action: Document where feature specs live and how tasks reference them.
        Acceptance: FILE_ORGANISATION.md references FEATURES_SPECIFICATION.md and task embedding.
        Context: docs/FILE_ORGANISATION.md

     Feature 4) + Add Features to all tasks in TASKS.md
        Action: Introduce a Features section for each task with appropriate statuses.
        Acceptance: All tasks list features; Task 13 marked complete.
        Context: tasks/TASKS.md

14) - Plans update
   Action: Update plans for all tasks and features.
   Acceptance: The file `docs/PLAN_SPECIFICATION.md` is updated to reflect what is the the expected behavior for an agent to carry out for each task. The file `docs/SPEC.md` is updated so that the first acton to do is to read the `docs/PLAN_SPECIFICATION.md`. The file `tasks/TASKS.md` is updated to reflect the changes made to the `docs/PLAN_SPECIFICATION.md`, including any updates to the actions and acceptance criteria.
   Notes: Each agent must always first compose a plan for a task before executing it. This in turn means that the plan must also encompass all features that a task is composed of. This is the only way to ensure that the agent can execute a task correctly.
   Context: docs/PLAN_SPECIFICATION.md, tasks/TASKS.md, docs/SPEC.md

   Features:
     Feature 1) - Update PLAN_SPECIFICATION.md for feature-aware planning
        Action: Explicitly require coverage of task features in the plan.
        Acceptance: PLAN_SPECIFICATION.md includes a section on planning across features.
        Context: docs/PLAN_SPECIFICATION.md

     Feature 2) - Update SPEC.md ACTIONS to read plan spec first
        Action: Make the first action: read docs/PLAN_SPECIFICATION.md.
        Acceptance: SPEC.md updated accordingly.
        Context: docs/SPEC.md

     Feature 3) - Align TASKS.md to new plan process
        Action: Ensure tasks/acceptance reflect plan-first, feature-aware execution.
        Acceptance: TASKS.md updated where needed.
        Context: tasks/TASKS.md

15) - Cleanup
   Action: Ensure that everything follows all current specifications. Look at all the files provided in the context, the current tasks, features and plans. Ensure that there are no inconsistencies between the files and that the files are up to date.
   Context: docs/SPEC.md, docs/TASK_FORMAT.md, docs/FILE_ORGANISATION.md, tasks/TASKS.md, docs/PLAN_SPECIFICATION.md, docs/AGENT_PRINCIPLES.md, plans/, scripts/run_local_agent.py, requirements.txt, .env.example, LOCAL_SETUP.md

   Features:
     Feature 1) - Validate consistency across documents
        Action: Cross-check all docs vs their acceptance criteria.
        Acceptance: Discrepancies are identified and fixed.
        Context: All listed files

     Feature 2) - Normalize statuses and references
        Action: Ensure statuses and references match actual repo state.
        Acceptance: No dangling or conflicting references.
        Context: tasks/TASKS.md

     Feature 3) - Apply Self-Cleaning principle
        Action: Remove obsolete content superseded by newer specs.
        Acceptance: Obsolete references are removed in the same change that introduces the replacement.
        Context: docs/SPECIFICATION_GUIDE.md

16) ? Running in isolation/container
   Action: Create a workflow to running the agent in a container, i.e. isolated environment.
   Acceptance: The file `RUNNING_IN_CONTAINER.md` exists detailing the steps involved in running the agent in a container environment.
   Context: scripts/run_local_agent.py
   Notes: The purpose is to have an agent periodically run in a container and not affect the host machine.

   Features:
     Feature 1) ? Explore containerization approaches
        Action: Evaluate Docker, Podman, and minimal base images.
        Acceptance: Pros/cons documented; recommendation selected.
        Context: docs/FEATURES_SPECIFICATION.md

     Feature 2) ? Author Dockerfile and compose
        Action: Create Dockerfile and optional docker-compose for dev/prod.
        Acceptance: RUNNING_IN_CONTAINER.md references these files and usage.
        Context: RUNNING_IN_CONTAINER.md

     Feature 3) ? Define volumes and secrets
        Action: Specify volume mounts and env handling for keys.
        Acceptance: Guide includes secure handling of .env/.secrets.
        Context: RUNNING_IN_CONTAINER.md

16) ? Running on cloud
   Action: Create a workflow to running the agent on cloud services such as AWS or Azure.
   Acceptance: The file `RUNNING_ON_CLOUD.md` exists detailing the steps involved in running the agent on cloud services.
   Context: docs/RUNNING_IN_CONTAINER.md
   Notes: Once containerization is established, it should be possible to also host this project somewhere and have it perpetually run on a cloud service.

   Features:
     Feature 1) ? Evaluate cloud targets
        Action: Compare AWS, Azure, GCP for simplest hosting.
        Acceptance: Options and trade-offs listed; one chosen.
        Context: RUNNING_ON_CLOUD.md

     Feature 2) ? Deployment workflow
        Action: Define deploy steps (container registry, runner, scheduling).
        Acceptance: RUNNING_ON_CLOUD.md includes end-to-end steps.
        Context: RUNNING_ON_CLOUD.md

     Feature 3) ? Observability and cost
        Action: Define basic logging/monitoring and cost control.
        Acceptance: Guide includes minimal observability and budget notes.
        Context: RUNNING_ON_CLOUD.md

16) ? Run tests
   Action: Create a test framework for testing the agent's functionality.
   Acceptance: The file `TESTING.md` exists detailing the steps involved in testing the agent's functionality.
   Context: docs/AGENT_PRINCIPLES.md, docs/TOOL_ARCHITECTURE.md
   Notes: The test framework is implemented and can run tests on the agent - knowing the agent's output and the tools it can access, it needs to be able to determine if the agent has completed a task successfully or not.

   Features:
     Feature 1) ? Define test taxonomy
        Action: Identify unit, integration, and E2E tests for agent behaviors.
        Acceptance: TESTING.md defines scope and examples per category.
        Context: TESTING.md

     Feature 2) ? Implement harness for JSON contract
        Action: Validate agent JSON plan/tool_calls shape.
        Acceptance: Harness can fail malformed agent outputs.
        Context: docs/TOOL_ARCHITECTURE.md

     Feature 3) ? CI integration
        Action: Define how tests run in CI.
        Acceptance: CI steps documented; sample workflow provided.
        Context: .github/workflows (future)

17) ? Local app 
   Action: Create a local app to handle project management, see tasks etc.
   Acceptance: The file `LOCAL_APP.md` exists detailing the steps involved in creating a local app for project management
   Context: docs/SPEC.md
   Notes: Currently I'm using VSCode to view the project, run everything, see tasks etc. It would be ideal to have a dedicated app for managing the project, viewing tasks, seeing progress etc. For being able to see how the agents fares etc. Cline the plugin for VSCode does something like this and maybe it makes sense to even built upon a fork on this. One thing to keep in mind is that we want to be really third-party independent. If we can create something ourselves we should. The only question is how it integrates with the project. If maintaining such a service/dependency is too heavy, then using a third party solution makes sense. Each third party solution should be its own tasks, with documented features and explanations as to why it was chosen etc.

   Features:
     Feature 1) ? Define app scope and UI
        Action: Determine minimal viable views (tasks, features, plans).
        Acceptance: LOCAL_APP.md includes scope and wireframes.
        Context: LOCAL_APP.md

     Feature 2) ? Data model and sync
        Action: Decide how app reads/writes repo state.
        Acceptance: Read/write flow specified; safety considerations noted.
        Context: LOCAL_APP.md

     Feature 3) ? Technology selection
        Action: Evaluate frameworks (e.g., Tauri, Electron) vs plugin approach.
        Acceptance: Options listed; recommendation justified.
        Context: LOCAL_APP.md

18) ? Create a mobile app
    Action: Develop a mobile application that allows users to interact with the project and thus the agents it runs.
    Acceptance: The file `MOBILE_APP.md` exists detailing the development process and user interface design for the mobile application.
    Context: docs/LOCAL_APP.md
    Notes: The purpose of this is to allow users to interact with the agent through a mobile device. It could include voice commands, touch gestures, or other input methods depending on the target audience and platform.

   Features:
     Feature 1) ? App scope and UX
        Action: Define primary interactions and UX flows.
        Acceptance: MOBILE_APP.md outlines flows and mockups.
        Context: MOBILE_APP.md

     Feature 2) ? Offline and notifications strategy
        Action: Determine how the app syncs and notifies users.
        Acceptance: Strategy documented with trade-offs.
        Context: MOBILE_APP.md

     Feature 3) ? Technology selection
        Action: Evaluate cross-platform vs native approaches.
        Acceptance: Recommendation documented with rationale.
        Context: MOBILE_APP.md
