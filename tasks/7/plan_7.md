# Plan for Task 7: Agent Orchestrator

## Intent
Implement the local orchestrator script and setup, fully compliant with AGENT_PRINCIPLES and TOOL_ARCHITECTURE, including CLI options to run specific tasks/features and supporting local setup.

## Context
- Specs: `docs/AGENT_PRINCIPLES.md`, `docs/TOOL_ARCHITECTURE.md`, `docs/PLAN_SPECIFICATION.md`, `docs/FILE_ORGANISATION.md`

## Features
7.1) + Orchestrator script
   Action: Ensure scripts satisfies all requirements.
   Acceptance: Behavior matches `docs/TOOL_ARCHITECTURE.md` and `docs/AGENT_PRINCIPLES.md`.
   Output: `scripts/run_local_agent.py`
   Dependencies: 7.5, 7.6, 7.7

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

7.5) + Implement orchestrator script
   Action: Create `scripts/run_local_agent.py` that calls an agent specified by a model `--model {model_id}` with all system context files.
   Acceptance: Behavior matches `docs/TOOL_ARCHITECTURE.md` and `docs/AGENT_PRINCIPLES.md`. The script must accept as many possible models as possible.
   Output: `scripts/run_local_agent.py`
   Context: `docs/AGENT_PRINCIPLES.md`, `docs/TOOL_ARCHITECTURE.md`

7.6) - Orchestrator can parse and call tools
   Action: The script parses the agent's response JSON and in turn executes tools.
   Acceptance: An appropriate JSON response triggers a tool call.
   Output: `scripts/run_local_agent.py`
   Context: `docs/AGENT_PRINCIPLES.md`, `docs/TOOL_ARCHITECTURE.md`
   Dependencies: 7.5, 7.9, 7.10, 7.11, 7.12, 7.13, 7.14, 7.15

7.7) + Orchestrator supports Single/Continuous modes
   Action: The script has CLI options `--mode {mode_type}` where `mode_type` is either `single` (running just once) or `continuous` (running until there are no more tasks to work on).
   Acceptance: Behavior matches `docs/TOOL_ARCHITECTURE.md` and `docs/AGENT_PRINCIPLES.md`.
   Output: `scripts/run_local_agent.py`
   Context: `docs/AGENT_PRINCIPLES.md`, `docs/TOOL_ARCHITECTURE.md`
   Dependencies: 7.5

7.8) + Orchestrator can run specific task/feature
   Action: The script has CLI options `--task {task_id}` and `--feature {feature_id}` to run specific tasks/features via prompt construction referencing `tasks/plan_{task_id}.md`.
   Acceptance: Orchestrator accepts `--task` and optional `--feature` and executes accordingly; output confirms execution.
   Context: `docs/AGENT_PRINCIPLES.md`, `docs/TOOL_ARCHITECTURE.md`
   Dependencies: 7.5

7.9) + The tool for writing a file
   Action: Create a tool called `write_file` to write files.
   Acceptance: The tool uses correct naming and creates a file or rewrites an existing file.
   Output: `scripts/tools/write_file.py`
   Context: `docs/TOOL_ARCHITECTURE.md`

7.10) - The tool for getting project context file
   Action: Create a tool called `retrieve_context_files` to return wanted files as text and resume the agent's work.
   Acceptance: The tool uses correct naming and returns all files matching the pattern as text.
   Output: `scripts/tools/retrieve_context_files.py`
   Context: `docs/TOOL_ARCHITECTURE.md`
   Depdendencies: 7.15

7.11) + The tool for renaming files
   Action: Create a tool called `rename_files` to rename and move files.
   Acceptance: The tool uses correct naming and is able to rename existing files or move and potentially rename them.
   Output: `scripts/tools/rename_files.py`
   Context: `docs/TOOL_ARCHITECTURE.md`

7.12) + The tool for creating a git PR
   Action: Create a tool called `submit_for_review` to create Git Pull Requests, where the branch naming follows `features/{task_id}` or `features/{task_id}_{feature_id}` if `feature_id` is provided.
   Acceptance: The tool uses correct naming and creates a pull request. There is also a helper file that manages all git operations.
   Output: `scripts/tools/submit_for_review.py`, `scripts/git_manager.py`
   Context: `docs/TOOL_ARCHITECTURE.md`

7.13) + The tool for asking a question
   Action: Create a tool called `ask_question` to indicate an agent wanting to ask a question about a feature being worked on.
   Acceptance: The tool uses correct naming and is able to ask a question.
   Output: `scripts/tools/ask_question.py`
   Context: `docs/TOOL_ARCHITECTURE.md`

7.14) + The tool for finishing the task
   Action: Create a tool called `finish` to finish a task.
   Acceptance: The tool uses correct naming and is able to finish a task.
   Output: `scripts/tools/finish.py`
   Context: `docs/TOOL_ARCHITECTURE.md`

7.15) - The orchestrator can have a multi-way conversation with an LLM, not just one shot.
   Action: Update the orchestrator script to support multiple-shot conversations with an LLM.
   Acceptance: The orchestrator can handle multiple-shot conversations effectively. The tool `retrieve_context_files` can be called by the agent and it can resume its work.
   Output: `scripts/tools/retrieve_context_files.py`
   Context: `docs/TOOL_ARCHITECTURE.md`
   Dependencies: 7.5


## Execution Steps
1) Implement features
2) Update `tasks/TASKS.md` with status change
3) Submit for review
4) Finish
