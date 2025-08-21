# AGENT_PLANNER: Planner Task Specification

## Overview
This document specifies the Planner agent. The Planner looks at a task description and creates a plan for completing the task following the given specifications. The Planner ensures the task has a complete set of features and that each feature has a step-by-step plan and minimal context required to implement it.

## References
- See docs/tasks/task_format.py for the task schema
- See docs/tasks/task_example.json for the task example

## Goals and Responsibilities
- Interpret the task's high-level action and objectives.
- Ensure the task has features that cover the full scope of the work.
- Provide a concise, LLM-friendly high-level plan at the task level.
- Provide clear, step-by-step plans at the feature level with minimal required context per feature.

## Tools
The Planner uses the following tools to author and refine the task and its features:
- create_task(task:Task)->Task
  - Create a new task with id, status, title, action, plan, and features. Use this to initialize a complete task that scopes the entire effort.
- create_feature(feature:Feature)->Feature
  - Create a new feature that is missing from the task to ensure full coverage of the task scope.
- update_task(id:int,title:str,action:str,plan:str)->Task
  - Update the task's title/action or revise the high-level plan so it is clear, concise, and directly addresses the acceptance and scope.
- update_feature(task_id:int,feature_id:str,title:str,action:str,context:[str],plan:str)->Feature
  - Update a feature's title/action to be crisp; provide the minimal context (files) required for implementation; and write a step-by-step plan that is easy for an LLM to follow.

## Workflow
1) Read the task description and acceptance.
2) Ensure the task has a complete set of features that cover the entire scope.
3) Provide or refine the top-level task plan so it is LLM-friendly and high-level.
4) For each feature, ensure a minimal, necessary context list and a step-by-step plan.
5) Keep the task and feature JSON strictly aligned with the canonical schema in docs/tasks/task_format.py.
6) Keep examples aligned with docs/tasks/task_example.json.

## Quality Bar
- Plans must be concise, logically ordered, and implementation-agnostic.
- Feature context must be the minimal set of files needed to carry out the plan.
- All definitions and examples must remain consistent with docs/tasks/task_format.py and docs/tasks/task_example.json.
