# Plan for Task 7: Agent Orchestrator

## Intent
Create a functional orchestrator script that interacts with an LLM agent using the defined JSON contract and tool suite, enabling execution of tool calls in Single and Continuous modes. Provide the supporting rename_files tool. Mark the task complete once the script exists and adheres to the specification.

## Context
- Specs: docs/TOOL_ARCHITECTURE.md, docs/AGENT_PRINCIPLES.md, docs/PLAN_SPECIFICATION.md, docs/FEATURE_FORMAT.md, docs/TASK_FORMAT.md
- Source files to create: scripts/run_local_agent.py, scripts/rename_files.py

## Features
7.1) Implement Agent Orchestrator script
   Action: Create scripts/run_local_agent.py that provides context to the agent, enforces the JSON schema, exposes all tools, and executes tool calls. Support Single and Continuous modes and multiple providers (manual, OpenAI SDK if available, generic OpenAI-compatible HTTP).
   Acceptance:
   - scripts/run_local_agent.py exists
   - The script enforces the JSON response schema (plan + tool_calls)
   - The tools write_file, retrieve_context_files, rename_files, submit_for_review, ask_question, finish are implemented and executable
   - Supports --mode single|continuous and --provider manual|openai|http
   Context: docs/TOOL_ARCHITECTURE.md, docs/AGENT_PRINCIPLES.md
   Output: scripts/run_local_agent.py

7.2) Implement rename_files tool
   Action: Provide scripts/rename_files.py implementing safe in-repo move/rename with overwrite and dry-run options. Return a structured JSON result.
   Acceptance:
   - scripts/rename_files.py exists
   - rename_files(operations, overwrite, dry_run) returns JSON with ok, summary, results
   - Validates paths do not escape the repo root
   Context: docs/TOOL_ARCHITECTURE.md
   Output: scripts/rename_files.py

7.3) Document minimal provider configuration via CLI flags
   Action: Ensure orchestrator runs without external dependencies by default (manual provider) and optionally supports OpenAI SDK and HTTP provider if configured via environment variables.
   Acceptance:
   - Orchestrator runs with `--provider manual` without additional packages
   - OpenAI and HTTP providers are optional and only required if selected
   Context: docs/AGENT_PRINCIPLES.md

## Execution Steps
1) Create scripts/rename_files.py implementing the rename_files tool
2) Create scripts/run_local_agent.py implementing the orchestrator and tools per spec
3) Update tasks/TASKS.md to set Task 7 to completed with acceptance criteria
4) Submit for review and finish
