# Task Format Specification

## 1. Purpose
This document defines the canonical format for managing Tasks and their Features within this project. It is self-contained and unambiguous, specifying fields, status codes, core rules, examples, and authoring tips so any contributor can read and write tasks consistently.

## 2. Field Definitions
A Task entry in tasks/TASKS.md MUST include the following fields in order:
- ID and Status: A numeric ID followed by a status symbol and a short Title line.
  - Example: `12) - Plan specification`
- Action: A concise imperative statement describing the work to be done.
- Acceptance: The objective criteria that must be satisfied for the task to be considered complete.
- Notes: Optional clarifications, constraints, or hints.
- Dependencies: Optional list of task IDs that must be completed first.

A Feature entry in tasks/{task_id}/plan_{task_id}.md MUST include:
- Number and Status: `{task_id}.{n}) <status> <Feature Title>`
- Action: What the feature will implement.
- Acceptance: Verifiable criteria for completion.
- Context: Relevant files/specs to read before implementing the feature.
- Dependencies: Other features or tasks that must be completed first, if any.
- Output: The explicit file(s) or artifact(s) expected from the feature.
- Notes: Optional clarifications.

## 3. Statuses
Use the following status codes for both tasks and features:
- `+` Completed: All acceptance criteria are met and tests (if any) pass.
- `~` In Progress: Work has begun; do not start other features in parallel.
- `-` Pending: Not started yet; waiting for execution.
- `?` Needs Clarification: Requirements are ambiguous; ask questions before proceeding.
- `/` Blocked: Cannot proceed due to external dependency or failure; document the reason.
- `=` Deprecated/Obsolete: No longer needed or superseded by another task/feature.

Notes:
- A feature’s status should transition `-` → `~` → `+` in a single execution cycle whenever possible.
- A task can be marked `+` only when all its features are `+` and their tests pass.

## 4. Rules
### 4.1 Sequential Knowledge
- Tasks are ordered chronologically to reflect the project’s evolving knowledge.
- Later tasks may rely on artifacts or conventions established by earlier tasks.
- When introducing new concepts, prefer to update or reference the earliest relevant specification.

### 4.2 Non-Redundancy
- Do not duplicate content across files. Keep a single source of truth and reference it from other locations.
- If a section needs to be extended, update the canonical document and link to it rather than copying text.

### 4.3 Atomic Feature Execution
- One cycle = one feature = complete success. Implement exactly one pending feature per cycle, including its tests.
- Update feature status from `-` to `~` at start, then to `+` only after tests pass and the implementation meets acceptance.

### 4.4 Test-Driven Acceptance
- Every feature that produces tangible output must have a corresponding test under `tasks/{task_id}/tests/`.
- A feature is only done when its tests pass. See docs/PLAN_SPECIFICATION.md and docs/TESTING.md for details.

## 5. Examples
### 5.1 Task Entry (tasks/TASKS.md)
```
16) - Running in docker
   Action: Create a workflow for running the project in an isolated Docker environment.
   Acceptance: A README and Dockerfile exist under docs/docker/, and steps are documented to build and run the container.
   Notes: The agent should run in a container without impacting the host machine.
   Dependencies: 5
```

### 5.2 Feature Entry (tasks/{task_id}/plan_{task_id}.md)
```
16.1) - Create Dockerfile and base README
   Action: Author docs/docker/Dockerfile and docs/docker/RUNNING_DOCKER_README.md with build/run instructions.
   Acceptance: Both files exist with clear steps to build an image and run the agent.
   Context: docs/PLAN_SPECIFICATION.md, docs/TESTING.md
   Output: docs/docker/Dockerfile, docs/docker/RUNNING_DOCKER_README.md
```

## 6. Tips
- Write Actions in the imperative mood and Acceptance criteria as verifiable outcomes.
- Keep scope minimal and incremental; avoid bundling unrelated work.
- Prefer explicit file paths in Acceptance to enable deterministic tests.
- If context is missing or ambiguous, set status to `?` and ask a question before proceeding.
- Always update status markers accurately to reflect true progress.

## 7. Conformance Checklist
- Fields present and in the correct order.
- Status codes use the defined symbols and meanings.
- No duplicated content; references to canonical docs where appropriate.
- Tests exist for features that create or modify files and they pass.

This specification governs both the top-level task list (tasks/TASKS.md) and per-task feature plans (tasks/{task_id}/plan_{task_id}.md).
