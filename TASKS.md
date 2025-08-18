# Tasks

See **[TASK_FORMAT.md](TASK_FORMAT.md)** for format reference and how to write acceptance criteria.

## Current Tasks

1) + Initial spec document
   Action: Create the founding SPEC.md document
   Acceptance: SPEC.md exists with WHAT, CORE IDEAS and ACTIONS sections

2) = Specification documentation
   Action: Analyse the specification format and what requirements it needs to provide.
   Acceptance: SPECIFICATION_GUIDE.md exists describing format, SPEC.md adheres to this format

3) + First tasks
   Description: Create the initial task list for the project
   Acceptance: TASKS.md exists with at least 3 tasks and at least 1 pending task

4) = Task format
   Action: Analyse the tasks and what requirements they need to provide. All the format and specification for that should be included in the documentation.
   Acceptance: TASK_FORMAT.md exists describing the format, TASKS.md adheres to this format

5) = Specification template
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
    Acceptance: The file `requirements.txt` exists and contains the necessary libraries (`litellm`, `python-dotenv`).
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

13) - Task plans
   Action: Create a plan for each task.
   Acceptance: A folder /plans with a plan file for each task exists.
   Dependencies: 12
