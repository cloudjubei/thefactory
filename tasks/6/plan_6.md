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

## Execution Steps
1) Implement features
2) Update `tasks/TASKS.md` with status change
3) Submit for review
4) Finish
