# Plan for Task 6: Define Core Agent Terminology and Principles

## Intent
Establish core principles and define the agent's tool-based architecture and terminology.

## Context
- Specs: `docs/PLAN_SPECIFICATION.md`

## Features
6.1) + Create the tools guide
   Action: Specify the JSON contract, tools, and execution modes.
   Acceptance: `docs/TOOL_ARCHITECTURE.md` exists with all sections and tool definitions.
   Output: `docs/TOOL_ARCHITECTURE.md`

6.2) + Create the principles guide
   Action: Define Agent vs Orchestrator and core principles.
   Acceptance: `docs/AGENT_PRINCIPLES.md` exists and contains required definitions referencing the tools guide.
   Output: `docs/AGENT_PRINCIPLES.md`
   Context: `docs/PLAN_SPECIFICATION.md`, `docs/TOOL_ARCHITECTURE.md`
   Dependencies: 6.1

6.3) + Document agent personas
   Action: Author `docs/AGENT_PERSONAS.md` describing Manager, Planner, Tester, Developer personas, including objectives, constraints, prompts, minimal context, and instructions to run each via `scripts/run_local_agent.py`.
   Acceptance: `docs/AGENT_PERSONAS.md` exists with clear definitions and run examples; references `docs/TOOL_ARCHITECTURE.md` and `docs/AGENT_PRINCIPLES.md`.
   Context: `docs/PLAN_SPECIFICATION.md`, `docs/TOOL_ARCHITECTURE.md`, `scripts/run_local_agent.py`
   Output: `docs/AGENT_PERSONAS.md`

6.4) + Deprecate tasks 7 and 10 (merged into Task 6)
   Action: Update `tasks/TASKS.md` to mark tasks 7 (Agent Orchestrator) and 10 (Agent personas) as `=` Deprecated with notes referencing Task 6.
   Acceptance: `tasks/TASKS.md` shows tasks 7 and 10 as deprecated and pointing to Task 6 and relevant docs.
   Output: `tasks/TASKS.md`

## Execution Steps
1) Implement features
2) Update `tasks/TASKS.md` with status change
3) Submit for review
4) Finish
