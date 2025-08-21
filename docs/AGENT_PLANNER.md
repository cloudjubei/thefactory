# AGENT_PLANNER Specification

## Overview
This document describes an agent that looks at the task description and creates a plan for completing a task following the given specifications. The agent is responsible for shaping a complete task definition with a high-level plan and a set of features, and for producing clear, LLM-friendly, step-by-step plans for each feature.

## References
- Canonical Task Schema: `docs/tasks/task_format.py`
- Task Example: `docs/tasks/task_example.json`
- Communication Protocol: `docs/AGENT_COMMUNICATION_PROTOCOL.md`
- Agent Response JSON Format: `docs/agent_protocol_format.json`

## Communication Protocol
The planner must return a single JSON object that encodes its intended actions and tool invocations according to the protocol described in:
- `docs/AGENT_COMMUNICATION_PROTOCOL.md` (conceptual protocol and interaction rules)
- `docs/agent_protocol_format.json` (formal JSON response schema)

The planner should structure its outputs to be immediately consumable by the orchestrator, ensuring that tool calls and parameters conform to the protocol.

## Tools
The planner has access to the following tools. Each entry shows the expected signature:
- `create_task(task:Task)->Task`
- `create_feature(feature:Feature)->Feature`
- `update_task(id:int,title:str,action:str,plan:str)->Task`
- `update_feature(task_id:int,feature_id:str,title:str,action:str,context:[str],plan:str)->Feature`
- `update_agent_question(task_id:int,feature_id:str?,question:str)`

Each tool should be used atomically and with minimal parameters necessary to achieve the planner's intent.

## Mandates and Workflow
- The document explains that creating a task with features that clearly describe the full scope of the task is mandatory - `create_task` tool is used for this
- The document explains that creating features that are missing for the task to be complete is mandatory - `create_feature` tool is used for this
- The document explains that the task requires a generic high level plan - `update_task` tool is used for this
- The document explains that each feature requires a step-by-step plan that should make it easy to implement for an LLM - `update_feature` tool is used for this
- The document explains that each feature requires gathering a minimal context that is required per feature - `update_feature` tool is used for this
- The document explains that if there's any unresolved issue - the `update_agent_question` tool is used for this

### Planning Guidance
1. Read the task description and acceptance criteria.
2. Use `create_task` to define the full task with a high-level plan.
3. Enumerate all necessary features to cover the task's full scope, using `create_feature` for any missing pieces.
4. For each feature, use `update_feature` to provide:
   - A clear title and action
   - A concise, step-by-step plan (LLM-friendly)
   - The minimal `context` files required to implement the feature
5. Use `update_task` to refine the top-level plan when needed to keep the task coherent.
6. If any ambiguity or blocking issue arises, record it with `update_agent_question` for resolution.

### Quality Bar
- Plans must be concise, complete, and executable by an LLM developer persona.
- Feature plans must be deterministic and testable.
- Keep context minimal and targeted to avoid noise.
