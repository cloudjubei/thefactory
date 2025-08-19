# Plan for Task 6: Core Agent — Principles, Orchestrator, and Personas

## Intent
Consolidate the core agent foundations by defining principles and terminology, documenting the tool-based architecture, and integrating the Orchestrator and Personas into a single cohesive task.

## Context
- Specs: `docs/PLAN_SPECIFICATION.md`
- Tools Contract: `docs/TOOL_ARCHITECTURE.md`
- Principles: `docs/AGENT_PRINCIPLES.md`
- Personas: `docs/AGENT_PERSONAS.md`
- Orchestrator: `scripts/run_local_agent.py`

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

6.3) + Agent Orchestrator CLI and tool bridge
   Action: Provide a script that allows interaction with an agent and exposes SAFE tools per `docs/TOOL_ARCHITECTURE.md`.
   Acceptance: `scripts/run_local_agent.py` exists and supports the JSON contract, tool execution, persona mode routing, and single/continuous modes.
   Context: `docs/TOOL_ARCHITECTURE.md`, `docs/AGENT_PRINCIPLES.md`
   Dependencies: 6.1, 6.2
   Output: `scripts/run_local_agent.py`

6.4) + Agent Personas
   Action: Define Manager, Planner, Tester, and Developer personas with clear prompts and runnable modes.
   Acceptance: `docs/AGENT_PERSONAS.md` exists; `scripts/run_local_agent.py` supports running personas individually; `tasks/TASKS.md` is updated to reflect that personas are part of Task 6.
   Context: `docs/PLAN_SPECIFICATION.md`, `docs/FEATURE_FORMAT.md`, `docs/TOOL_ARCHITECTURE.md`, `docs/AGENT_PRINCIPLES.md`
   Dependencies: 6.3
   Output: `docs/AGENT_PERSONAS.md`, `scripts/run_local_agent.py`

## Execution Steps
1) Verify artifacts exist for features 6.1–6.4
2) Update `tasks/TASKS.md` to mark Task 6 as complete and deprecate Tasks 7 and 10 as merged
3) Submit for review
4) Finish
