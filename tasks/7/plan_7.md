# Plan for Task 7: Agent Orchestrator

## Intent
Implement the local orchestrator script and setup, fully compliant with AGENT_PRINCIPLES and TOOL_ARCHITECTURE, including CLI options to run specific tasks/features and supporting local setup.

## Context
- Specs: `docs/AGENT_PRINCIPLES.md`, `docs/TOOL_ARCHITECTURE.md`, `docs/PLAN_SPECIFICATION.md`, `docs/FILE_ORGANISATION.md`

## Features
7.1) - Orchestrator script
   Action: Ensure scripts satisfies all requirements.
   Acceptance: Behavior matches `docs/TOOL_ARCHITECTURE.md` and `docs/AGENT_PRINCIPLES.md`.
   Output: `scripts/run_local_agent.py`
   Dependencies: 7.6, 7.7, 7.8, 7.9, 7.10, 7.11, 7.12, 7.13, 7.14

7.2) + Dependency specification
   Action: Create `requirements.txt` listing all external libraries used by `scripts/run_local_agent.py`.
   Acceptance: `requirements.txt` exists and installs cleanly.
   Output: `requirements.txt`
   Context: `scripts/run_local_agent.py`
   Dependencies: 7.1

7.3) + Environment variables template
   Action: Provide `.env.example` containing placeholders for required API keys and settings.
   Acceptance: `.env.example` exists and documents each variable.
   Output: `.env.example`
   Context: `scripts/run_local_agent.py`
   Dependencies: 7.1

7.4) + Local setup guide
   Action: Author `docs/LOCAL_SETUP.md` with setup and execution instructions.
   Acceptance: `docs/LOCAL_SETUP.md` exists and is accurate.
   Output: `docs/LOCAL_SETUP.md`
   Context: `scripts/run_local_agent.py`, `requirements.txt`, `.env.example`
   Dependencies: 7.1, 7.2, 7.3

7.5) + Implement orchestrator script (Core Logic)
   Action: Create `scripts/run_local_agent.py` that calls an agent specified by a model `--model {model_id}` with all system context files.
   Acceptance: Behavior matches `docs/TOOL_ARCHITECTURE.md` and `docs/AGENT_PRINCIPLES.md`. The script must accept as many possible models as possible.
   Output: `scripts/run_local_agent.py`
   Context: `docs/AGENT_PRINCIPLES.md`, `docs/TOOL_ARCHITECTURE.md`
   Notes: This feature reflects the core implementation of the orchestrator, which is largely complete.

7.6) + Orchestrator can parse and call tools
   Action: The script parses the agent's response JSON and in turn executes tools.
   Acceptance: An appropriate JSON response triggers a tool call.
   Output: `scripts/run_local_agent.py`
   Context: `docs/AGENT_PRINCIPLES.md`, `docs/TOOL_ARCHITECTURE.md`
   Dependencies: 7.5, 7.9, 7.10, 7.11, 7.12, 7.13, 7.14

7.7) + Orchestrator supports Single/Continuous modes
   Action: The script supports Single/Continuous modes.
   Acceptance: Behavior matches `docs/TOOL_ARCHITECTURE.md` and `docs/AGENT_PRINCIPLES.md`.
   Output: `scripts/run_local_agent.py`
   Context: `docs/AGENT_PRINCIPLES.md`, `docs/TOOL_ARCHITECTURE.md`
   Dependencies: 7.5

7.8) - Orchestrator can run specific task/feature
   Action: The script has CLI options `--task-id {task_id}` and `--feature-id {feature_id}` to run specific tasks/features via prompt construction referencing `tasks/plan_{task_id}.md`.
   Acceptance: Orchestrator accepts `--task-id` and optional `--feature-id` and executes accordingly; output confirms execution.
   Context: `docs/AGENT_PRINCIPLES.md`, `docs/TOOL_ARCHITECTURE.md`
   Dependencies: 7.5

7.9) + The tool for writing a file (`write_file`)
   Action: Create a tool called `write_file` to write files.
   Acceptance: The tool uses correct naming and creates a file or rewrites an existing file.
   Output: `scripts/run_local_agent.py` (as part of AgentTools)
   Context: `docs/TOOL_ARCHITECTURE.md`
   Notes: The plan initially specified `scripts/tools/write_file.py` but the implementation is directly within `scripts/run_local_agent.py`'s `AgentTools` class, which is compliant with `docs/TOOL_ARCHITECTURE.md`.

7.10) + The tool for getting project context files (`retrieve_context_files`)
   Action: Create a tool called `retrieve_context_files` to return wanted files as text and resume the agent's work.
   Acceptance: The tool uses correct naming and returns all files matching the pattern as text.
   Output: `scripts/run_local_agent.py` (as part of AgentTools)
   Context: `docs/TOOL_ARCHITECTURE.md`
   Notes: Implemented directly within `scripts/run_local_agent.py`'s `AgentTools` class.

7.11) + The tool for renaming files (`rename_files`)
   Action: Create a tool called `rename_files` to rename and move files.
   Acceptance: The tool uses correct naming and is able to rename existing files or move and potentially rename them.
   Output: `scripts/rename_files.py` (and called via AgentTools in `scripts/run_local_agent.py`)
   Context: `docs/TOOL_ARCHITECTURE.md`
   Notes: The core logic is in `scripts/rename_files.py` as noted in `docs/TOOL_ARCHITECTURE.md`.

7.12) + The tool for creating a git PR (`submit_for_review`)
   Action: Create a tool called `submit_for_review` to create Git Pull Requests, where the branch naming follows `agent/cycle-{run_count}` as implemented.
   Acceptance: The tool uses correct naming and creates a pull request.
   Output: `scripts/run_local_agent.py` (as part of AgentTools)
   Context: `docs/TOOL_ARCHITECTURE.md`
   Notes: Implemented directly within `scripts/run_local_agent.py`'s `AgentTools` class.

7.13) + The tool for asking a question (`ask_question`)
   Action: Create a tool called `ask_question` to indicate an agent wanting to ask a question about a feature being worked on.
   Acceptance: The tool uses correct naming and is able to ask a question.
   Output: `scripts/run_local_agent.py` (as part of AgentTools)
   Context: `docs/TOOL_ARCHITECTURE.md`
   Notes: Implemented directly within `scripts/run_local_agent.py`'s `AgentTools` class.

7.14) + The tool for finishing the task (`finish`)
   Action: Create a tool called `finish` to finish a task.
   Acceptance: The tool uses correct naming and is able to finish a task.
   Output: `scripts/run_local_agent.py` (as part of AgentTools)
   Context: `docs/TOOL_ARCHITECTURE.md`
   Notes: Implemented directly within `scripts/run_local_agent.py`'s `AgentTools` class.

## Execution Steps
1) Implement features
2) Update `tasks/TASKS.md` with status change
3) Submit for review
4) Finish
