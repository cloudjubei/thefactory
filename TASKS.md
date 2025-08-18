# Tasks

See **[TASK_FORMAT.md](TASK_FORMAT.md)** for format reference and how to write acceptance criteria.

## Current Tasks

0) + Initial spec document
   Action: Create the founding SPEC.md document
   Acceptance: SPEC.md exists with WHAT, CORE IDEAS and ACTIONS sections

1) = Specification documentation
   Action: Analyse the specification format and what requirements it needs to provide.
   Acceptance: SPECIFICATION_GUIDE.md exists describing format, SPEC.md adheres to this format

2) + First tasks
   Description: Create the initial task list for the project
   Acceptance: TASKS.md exists with at least 3 tasks and at least 1 pending task

3) = Task format
   Action: Analyse the tasks and what requirements they need to provide. All the format and specification for that should be included in the documentation.
   Acceptance: TASK_FORMAT.md exists describing the format, TASKS.md adheres to this format

4) = Specification template
   Action: Create a reusable template for writing new specifications
   Acceptance: TEMPLATE.md exists with all required sections from SPECIFICATION_GUIDE.md, with examples for each
   Dependencies: 1

5) - Allow Autonomous Agents to produce changes
   Action: Create a workflow so that an AI agent can create a change to the project (relating to a task) by committing them and creating a Pull Request for it to be reviewed.
   Acceptance: A commit with some changes is made and a Pull Request is opened for it.
   Dependencies: 2,6,7,8,9

6) + Specify the Autonomous Agent Workflow
   Action: Define the step-by-step process an autonomous agent will follow to select a task, make changes to the repository, and create a pull request. This specification should also define the tools and permissions the agent will require.
   Acceptance: AGENT_WORKFLOW.md exists, detailing the agent's decision-making process, how it interacts with the git repository, and the format of its pull requests.

7) + Implement a Basic Git Interaction Script for the Agent
    Action: Create a script that can perform the basic git operations required for the autonomous agent. This includes cloning the repository, creating a new branch, committing changes, and pushing the branch to the remote repository.
    Acceptance: A script, git_manager.py, is created in the scripts/ directory. The script can be manually triggered to perform the specified git operations.
    Dependencies: 6

8) + Set up a GitHub Action to Automate the Agent's Workflow
    Action: Create a GitHub Actions workflow that automates the execution of the agent's tasks. This workflow should be triggerable on a specific event (e.g., a new issue being labeled for the agent).
    Acceptance: A new workflow file, agent_workflow.yml, is added to the .github/workflows/ directory. This workflow successfully runs the git interaction script and creates a pull request.
    Dependencies: 7

9) - Test Agent Automation
   Action: This is a test task for the GitHub Actions workflow to pick up.
   Acceptance: The agent creates a file named `task_9_output.md`, commits it and opens a PR.

10) + Fully Automate Agent Trigger
    Action: Modify the GitHub Action workflow to run on an automatic schedule instead of a manual trigger, enabling true autonomy.
    Acceptance: The `agent_workflow.yml` trigger is changed from `workflow_dispatch` to a `schedule` (cron).
    Dependencies: 8

11) - Verify Full Automation
    Action: A new test task for the fully automated, schedule-triggered agent to execute.
    Acceptance: The scheduled agent creates a file named `task_11_output.md`, updates this task's status to `~`, and opens a pull request.
    Dependencies: 10

12) - Enhance Git Script for PR Creation
    Action: Extend the `scripts/git_manager.py` script to include a new method, `create_pull_request`. This method will use the GitHub CLI (`gh`) to create a pull request on the remote repository.
    Acceptance: The `git_manager.py` script has a new `create_pull_request` method that, when called, successfully creates a pull request on GitHub.
    Dependencies: 7
    Output: Modified `scripts/git_manager.py`

13) - Create Local Agent Orchestration Script
    Action: Create a new main agent script at `scripts/run_local_agent.py`. This script will be the single entry point for a human to run the agent. It will be responsible for: 1. Parsing `TASKS.md` to find an eligible task. 2. Calling the `GitManager` to set up a new branch. 3. Performing the file modifications required by the task. 4. Calling the `GitManager` to commit, push, and create a pull request.
    Acceptance: Running `python3 scripts/run_local_agent.py` in the terminal successfully finds a pending task, creates a branch, commits file changes, pushes, and opens a pull request on GitHub.
    Dependencies: 12
    Output: `scripts/run_local_agent.py`

14) - Specify Unified LLM Engine Architecture
    Action: Create a new specification that replaces the dual-engine design with a single, unified engine powered by the `LiteLLM` library. This spec must also define the use of a `requirements.txt` file for dependencies and a `.env` file for API key management.
    Acceptance: `UNIFIED_ENGINE.md` exists, detailing the new architecture.

15) - Implement Dependency and Configuration Management
    Action: Create the `requirements.txt` file listing all Python dependencies (`litellm`, `python-dotenv`). Create a `.env.example` file to serve as a template for users' API keys.
    Acceptance: `requirements.txt` and `.env.example` files are created in the root directory.
    Dependencies: 14

16) - Refactor Agent to use a Unified LiteLLM Engine
    Action: Completely refactor `scripts/run_local_agent.py`. Remove all direct calls to `requests` and `google.generativeai`. Implement a single `UnifiedEngine` class that uses `litellm` to handle all model calls. The `--provider` flag will now select a model string (e.g., 'ollama/llama3' or 'gemini/gemini-1.5-flash').
    Acceptance: The agent is refactored to use a single engine. The code is simpler and no longer contains provider-specific logic.
    Dependencies: 15
    Output: Modified `scripts/run_local_agent.py`

17) - Create Finalized Setup and Usage Guide
    Action: Completely rewrite `LOCAL_SETUP.md` from scratch. It must include the correct `brew services` command for Ollama, instructions for installing dependencies via `pip3 install -r requirements.txt`, and a clear guide on setting up the `.env` file from the example.
    Acceptance: The new `LOCAL_SETUP.md` is accurate, easy to follow, and allows a new user to run the agent successfully.
    Dependencies: 16
    Output: `LOCAL_SETUP.md`


18) - Fix TypeError in Task Parser
    Action: Resolve a `TypeError` in the `_parse_tasks` method by passing a string instead of a list to `re.match`.
    Acceptance: The agent no longer crashes when parsing `TASKS.md`.

19) - Specify Agent-Led Task Execution
    Action: Update the agent's principles to specify that the LLM, not the orchestrator script, is responsible for selecting the next task to execute. The script's role is to provide full context and execute the LLM's directives.
    Acceptance: `AGENT_PRINCIPLES.md` is updated to reflect this new, more powerful agent architecture.
    Dependencies: 18

20) - Implement Agent-Led Orchestrator
    Action: Refactor `run_local_agent.py`. Remove the `_find_eligible_task` method and any task-selection logic. Simplify the main `run` loop to make a single call to the LLM with the full project context, asking it to determine and perform the next action.
    Acceptance: The Python script no longer contains any logic for choosing a task.
    Dependencies: 19
    Output: Modified `scripts/run_local_agent.py`

21) + Fix AttributeError in LiteLLM Response Parsing
    Action: Resolve an `AttributeError` by correctly accessing the `response.choices[0]` index.
    Acceptance: The agent no longer crashes when parsing a LiteLLM response.

22) - Specify Tool-Using Agent Architecture
    Action: Create a new specification document that redefines the agent's output. The agent will now respond with a JSON object containing a list of "tool calls" (e.g., `write_file`, `run_shell_command`). Define the exact JSON schema and the initial set of available tools.
    Acceptance: `TOOL_ARCHITECTURE.md` exists and clearly defines the new agent-orchestrator contract.

23) - Implement Tool-Calling Orchestrator
    Action: Heavily refactor `run_local_agent.py`. The main loop will no longer perform git operations itself. Instead, it will parse the LLM's JSON response and execute the specified tool calls in sequence.
    Acceptance: The orchestrator can parse a JSON response from the LLM and call the corresponding Python functions.
    Dependencies: 22
    Output: Modified `scripts/run_local_agent.py`

24) - Update System Prompt for Tool Usage
    Action: Rewrite the system prompt in `run_local_agent.py`. The new prompt must explicitly instruct the LLM on how to use the available tools, the required JSON output format, and its new goal: to create a full plan of action from file edits to creating a pull request.
    Acceptance: The agent's prompt clearly defines the tool-use paradigm.
    Dependencies: 23
    Output: Modified `scripts/run_local_agent.py`