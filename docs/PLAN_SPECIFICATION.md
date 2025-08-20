# Plan Specification

## 1. Purpose
A "plan" is the AI Agent's high-level, human-readable strategy for completing a given task. It is generated before any tool calls are executed. The plan outlines the agent's interpretation of the task, the steps it will take, and the final output it intends to produce. It serves as a clear statement of intent. The plan for a task and its features is stored directly within the `plan` field of the corresponding `tasks/{task_id}/task.json` file.

## 2. Core Principles
Every plan must adhere to the following principles:

### 2.1. Task-Driven
The plan must directly address the `Action` and `Acceptance` criteria of the target task from `tasks/{task_id}/task.json`. The primary goal of the plan is to satisfy these criteria completely.

### 2.2. Atomic Execution
The plan represents a single, atomic set of actions that will be executed. The agent formulates the entire plan and all corresponding tool calls in one turn. Therefore, the plan should describe a complete unit of work, from start to finish.

### 2.3. Logical Sequence
The steps in the plan should follow a clear, logical progression:
1. Analysis: Start by interpreting the task's requirements.
2. Creation/Modification: Detail the primary changes to be made (e.g., creating new files, modifying existing ones).
3. Administration: Include the final administrative steps, such as updating the task status and submitting the work for review.

### 2.4. Clarity and Brevity (LLM-Friendly)
- Plans must be written in Markdown using headings and short bulleted/numbered steps.
- Keep sentences concise and action-oriented.
- Reference files with exact relative paths and tools by their exact names.
- Avoid ambiguity; each step should map to tool calls and acceptance checks.

### 2.5. Test-Driven Acceptance
A feature is not considered complete until a corresponding test is written and passes. This ensures that all work is verifiable.
- For every feature that produces a tangible output (like a file or a change in a file), a subsequent feature in the plan MUST be created to write a test for it.
- The acceptance criteria for the "test-writing" feature is that the test script exists under `tasks/{task_id}/tests/` and verifies the acceptance criteria of the previous feature.
- Use the `run_tests` tool to execute all tests and ensure they pass before submitting the work. This process is detailed further in `docs/TESTING.md`.

### 2.6. Per-Feature Single-Step Delivery and Commit (Required)
- The agent should complete each feature as a single cohesive step: gather all necessary context, implement the change, and finish by writing the tests for that feature.
- After tests pass, the agent MUST send `finish_feature` to create a per-feature commit.

### 2.7. Cohesive Context Per Feature (Required)
Before making any change for a feature, the agent MUST gather the Minimum Cohesive Context using `retrieve_context_files`.

### 2.8. Atomic Feature Execution
Exactly one feature per execution cycle.

## 3. Location and Structure
- Each task's definition, including its plan and features, is located at `tasks/{task_id}/task.json`.
- The `plan` field in the JSON contains the overall intent in Markdown, while each feature object contains its own detailed Markdown plan.

Template:
```
{
  "id": 99,
  "status": "-",
  "title": "Example Task Title",
  "action": "High-level action for the entire task.",
  "plan": """
### Intent
High-level strategy in Markdown.

### Steps
1. Do thing A.
2. Do thing B.
""",
  "acceptance": [
    {"phase": "Phase 1", "criteria": ["Criterion 1."]}
  ],
  "features": [
    {
      "id": "99.1",
      "status": "-",
      "title": "First Feature",
      "action": "Action for the first feature.",
      "acceptance": ["First acceptance criterion."],
      "plan": """
### Intent
Implement feature in Markdown.

### Steps
1. Implement.
2. Test.
3. Finish feature.
"""
    }
  ]
}
```

## 4. Example
See the template above.

## 5. Testing
Refer to docs/TESTING.md for writing and running tests.

## 6. Feature Completion Protocol (finish_feature)
Follow the Single Feature Cycle and Finalization steps. Use `update_feature_status` tool for atomic status updates.
