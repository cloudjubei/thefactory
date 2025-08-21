# Planner Task Plan Specification

This document specifies how the Planner persona creates and maintains a task plan that scopes the full work, aligns with the canonical schema, and is easy for an LLM to execute.

## References
- Task schema: docs/tasks/task_format.py
- Example task: docs/tasks/task_example.json
- Authoring guidance: docs/tasks/TASKS_GUIDANCE.md
- Tooling: docs/TOOL_ARCHITECTURE.md
- Agent principles: docs/AGENT_PRINCIPLES.md
- Planner persona: docs/AGENT_PERSONAS_PLANNER.md

## Core Requirements
- Creating a task with features that clearly describe the full scope of the task is mandatory.
- The task requires a generic high level plan.
- Each feature requires a step-by-step plan that should make it easy to implement for an LLM.
- Each feature requires gathering a minimal context that is required per feature.

## Structure and Content
1) Top-level Task Plan
- Provide a concise, high-level plan describing the overall strategy to complete the task.
- Ensure the plan aligns with the task action and acceptance.

2) Feature Plans
- For each feature, write a short, ordered, step-by-step plan focused on the what/why of changes.
- Include a minimal context list for files strictly necessary to implement the feature.
- Each feature must include atomic acceptance criteria that are verifiable via deterministic tests.

3) Status, Dependencies, and Consistency
- Use the schema from docs/tasks/task_format.py to shape all data.
- Declare feature dependencies when order matters.
- Keep the example in docs/tasks/task_example.json in mind for structure and naming.

## Workflow Notes for the Planner
- Plans should be LLM-friendly and avoid ambiguous phrasing.
- Plans must not duplicate the canonical schema; reference it instead.
- Plans should enable the Tester to derive acceptance criteria and tests, and the Developer to implement features with minimal ambiguity.
