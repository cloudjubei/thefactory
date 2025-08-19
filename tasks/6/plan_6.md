# Plan for Task 6: Define Core Agent Terminology, Orchestrator, and Personas

## Intent
Establish core principles and define the agent's tool-based architecture and terminology, consolidating the Orchestrator and Personas into a single cohesive task.

## Context
- Specs: `docs/PLAN_SPECIFICATION.md`, `docs/TASK_FORMAT.md`, `docs/TOOL_ARCHITECTURE.md`

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

6.3) - Consolidate Orchestrator scope under Task 6
   Action: Merge the Orchestrator (former Task 7) into Task 6 and remove Task 7 from `tasks/TASKS.md`. If any plan or tests exist under `tasks/7`, migrate or delete them appropriately under `tasks/6`.
   Acceptance: `tasks/TASKS.md` no longer includes Task 7; this plan references `scripts/run_local_agent.py`; any `tasks/7/*` artifacts are removed or merged; no dangling references remain.
   Context: `tasks/TASKS.md`; `scripts/run_local_agent.py`; `docs/TOOL_ARCHITECTURE.md`; `docs/TASK_FORMAT.md`
   Dependencies: 6.1, 6.2
   Output: Updated `tasks/TASKS.md`; updated `tasks/6/plan_6.md`; repository cleanup of `tasks/7/*` if present.

6.4) - Define and document Agent Personas
   Action: Author `docs/AGENT_PERSONAS.md` detailing Manager, Planner, Tester, Developer personas with objectives, constraints, primary tools, and example prompts. Ensure `run_local_agent.py` exposes persona mode to run each individually.
   Acceptance: `docs/AGENT_PERSONAS.md` exists with the four personas and clear prompts; `scripts/run_local_agent.py` supports `--persona` with minimal context per persona as described; I can run each persona individually for any task.
   Context: `scripts/run_local_agent.py`; `docs/PLAN_SPECIFICATION.md`; `docs/FEATURE_FORMAT.md`; `docs/TOOL_ARCHITECTURE.md`; `docs/AGENT_PRINCIPLES.md`
   Dependencies: 6.3
   Output: `docs/AGENT_PERSONAS.md`; updated `scripts/run_local_agent.py` if needed.

6.5) - Deprecate Task 12 after merge
   Action: Mark Task 12 as `=` Deprecated/Obsolete in `tasks/TASKS.md` with a note that the merge was performed in Task 6.
   Acceptance: `tasks/TASKS.md` shows Task 12 with `=` status and explanatory note; no conflicting instructions remain.
   Context: `tasks/TASKS.md`; `docs/TASK_FORMAT.md`
   Dependencies: 6.3
   Output: Updated `tasks/TASKS.md`

## Execution Steps
1) Implement features
2) Update `tasks/TASKS.md` with status change
3) Submit for review
4) Finish
