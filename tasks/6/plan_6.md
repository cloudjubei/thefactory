# Plan for Task 6: Agent Orchestration and Principles

## Intent
To establish a common vocabulary and guiding principles for the agent project, and create the main script that runs the agent and executes its commands.

## Features
6.1) - Define "Agent" and "Orchestrator"
   Action: Write definitions for these key terms.
   Acceptance: The terms are defined in `docs/AGENT_PRINCIPLES.md`.

6.2) - Document Core Principles
   Action: Outline the core principles like "Specification-Driven" and "LLM-Led Intelligence".
   Acceptance: The principles are documented in `docs/AGENT_PRINCIPLES.md`.

6.3) - Create run_local_agent.py script
   Action: Create the main entry point script.
   Acceptance: `scripts/run_local_agent.py` exists.

6.4) - Implement tool calling logic
   Action: Add logic to parse JSON from the agent and call the specified tools.
   Acceptance: The orchestrator can execute `write_file` and `finish` tools.