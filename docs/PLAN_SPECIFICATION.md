# Plan Specification

## 1. Purpose
A "plan" is the AI Agent's high-level, human-readable strategy for completing a given task. It is generated before any tool calls are executed. The plan outlines the agent's interpretation of the task, the steps it will take, and the final output it intends to produce. It serves as a clear statement of intent.

## 2. Core Principles
Every plan must adhere to the following principles:

### 2.1. Task-Driven
The plan must directly address the `Action` and `Acceptance` criteria of the target task from `TASKS.md`. The primary goal of the plan is to satisfy these criteria completely.

### 2.2. Atomic Execution
The plan represents a single, atomic set of actions that will be executed. The agent formulates the entire plan and all corresponding tool calls in one turn. Therefore, the plan should describe a complete unit of work, from start to finish.

### 2.3. Logical Sequence
The steps in the plan should follow a clear, logical progression:
1. Analysis: Start by interpreting the task's requirements.
2. Creation/Modification: Detail the primary changes to be made (e.g., creating new files, modifying existing ones).
3. Administration: Include the final administrative steps, such as updating `TASKS.md` and submitting the work for review.

### 2.4. Clarity and Brevity
The plan should be easy for a human to understand. It should be concise and focus on the "what" and "why," not the low-level "how." The implementation details are found in the content of the `write_file` tool calls, not in the plan itself.

### 2.5. Test-Driven Acceptance
A feature is not considered complete until a corresponding test is written and passes. This ensures that all work is verifiable.
- For every feature that produces a tangible output (like a file or a change in a file), a subsequent feature in the plan MUST be created to write a test for it.
- The acceptance criteria for the "test-writing" feature is that the test script exists under `tasks/{task_id}/tests/` and verifies the acceptance criteria of the previous feature.
- Use the `run_tests` tool to execute all tests and ensure they pass before submitting the work. Locally, `scripts/run_tests.py` may be invoked by the orchestrator's tool.

### 2.6. Per-Feature Single-Step Delivery and Commit (Required)
To enforce more thorough planning and reliable delivery:
- The agent should complete each feature as a single cohesive step: gather all necessary context, implement the change, and finish by writing the tests for that feature.
- When a feature is complete and its tests pass, the agent MUST send the `finish_feature` tool call. This triggers the orchestrator to commit the current work for that feature (creating one commit per feature) and push the branch.
- After all features in the task are completed and all tests pass, the agent submits the task via a pull request.

Note: The `finish_feature` tool is a dedicated completion signal for a feature. It is separate from the final `submit_for_review` and `finish` calls that complete the task.

### 2.7. Cohesive Context Per Feature (Required)
Before making any change for a feature, the agent MUST gather the Minimum Cohesive Context (MCC) required to execute that feature safely and correctly.

- Always use `retrieve_context_files` to fetch the MCC at the start of the feature.
- If the MCC is ambiguous or incomplete, use `ask_question` to clarify before proceeding.

MCC Checklist (adapt as needed per feature):
- tasks/TASKS.md
- The current task plan file: `tasks/{task_id}/plan_{task_id}.md`
- All specification files referenced in the feature's Context section (e.g., `docs/PLAN_SPECIFICATION.md`, `docs/FEATURE_FORMAT.md`, `docs/TOOL_ARCHITECTURE.md`, etc.)
- Any source files the feature will modify or read
- Relevant tool files the feature will use (e.g., under `scripts/tools/`)

Rationale: Ensures decisions are made with the most relevant information at hand, reduces rework, and aligns with the Specification-Driven approach.

### 2.8. Atomic Feature Execution
The agent MUST work on exactly ONE feature per execution cycle. This principle ensures:
- Complete context gathering for each feature
- Proper status tracking
- Reliable test creation and validation
- Predictable progress tracking

**Rule: One Cycle = One Feature = Complete Success**

## 3. Location and Structure
- Each task MUST have a dedicated plan file located at `tasks/{task_id}/plan_{task_id}.md`.
- The plan enumerates the FEATURES that make up the task. Each feature follows `docs/FEATURE_FORMAT.md`.

A plan should include the following sections:
- Title and Task Reference
- Intent and Scope
- Context: Links to relevant specs and files
- Features: Enumerated list using `{task_id}.{n}` numbering
- Execution Steps: A short ordered list mapping to tool calls
- Administrative Steps: Update `TASKS.md`, `submit_for_review`, `finish`

## 4. Template

```
# Plan for Task {task_id}: {Task Title}

## Intent
Short, high-level description of how this plan will satisfy the task's Acceptance criteria.

## Context
- Specs: docs/SPEC.md, docs/TASK_FORMAT.md, docs/PLAN_SPECIFICATION.md, docs/FEATURE_FORMAT.md, docs/TESTING.md
- Source files: (if any)

## Features
{task_id}.1) - Feature title
   Action: ...
   Acceptance: ...
   Context: ...
   Dependencies: ...
   Output: ...
   Notes: ...

## Execution Steps
For each feature in order:
1) Gather context (MCC) using `retrieve_context_files` and implement the feature changes
2) Create the test(s) that verify the feature's acceptance criteria under `tasks/{task_id}/tests/`
3) Run tests using the `run_tests` tool and ensure tests pass
4) Call `finish_feature` with a descriptive message (e.g., "Feature {task_id}.{n} complete: {Title}") to create a commit for this feature

After all features are completed:
5) Run `run_tests` again and ensure the full suite passes
6) Update `tasks/TASKS.md` with status change for this task
7) Submit for review (open PR)
8) Finish
```

## 5. Example

For a task like:
```
12) - Plan specification
    Action: Create a plan specification that describes how each task should be executed.
    Acceptance: The file `PLAN_SPECIFICATION.md` exists and details the steps involved in creating a task plan.
```

A good corresponding plan would be:

1. Analyze Task: Review Task 12 to confirm the goal is to create `docs/PLAN_SPECIFICATION.md` with purpose, principles, structure, template, and example.
2. Draft Specification: Author the content for `docs/PLAN_SPECIFICATION.md` covering purpose, principles, structure, template, and example.
3. Implement Per-Feature Flow: For each feature, write its tests, run the test suite using the `run_tests` tool, and then call `finish_feature` to create a per-feature commit.
4. Update Task List: Modify `tasks/TASKS.md` to change the status of Task 12 from `-` (Pending) to `+` (Completed).
5. Execute Changes: Generate the necessary tool calls:
   a. `write_file` to create `docs/PLAN_SPECIFICATION.md` with the drafted content.
   b. `write_file` to update `tasks/TASKS.md`.
   c. `submit_for_review` to finalize the task.
   d. `finish` to end the operation.

## 6. Testing

### 6.1 Purpose
Testing encodes the acceptance criteria into executable checks, making feature completion objective and reproducible.

### 6.2 Location
- All tests for a specific task reside within that task's folder under `tasks/{task_id}/tests/`.

### 6.3 Naming
- Each test file validating a specific feature should follow: `test_{task_id}_{feature_id}.py`.
  - Example: The test for Task 9, Feature 1 is `tasks/9/tests/test_9_1.py`.

### 6.4 Structure and Content
- Tests should be simple Python scripts that:
  - Verify file existence, expected structure, or key phrases defined by acceptance criteria.
  - Print PASS/FAIL messages and exit with 0 on success, 1 on failure.

Example:
```
import os, sys

def run():
    path = "docs/TEMPLATE.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    required = ["# Problem Statement", "# Inputs and Outputs"]
    missing = [s for s in required if s not in content]
    if missing:
        print("FAIL: Missing sections: " + ", ".join(missing))
        sys.exit(1)
    print("PASS: TEMPLATE.md has required sections.")
    sys.exit(0)

if __name__ == "__main__":
    run()
```

### 6.5 Running Tests
- Use the `run_tests` tool to execute tests and collect results.
- A feature can only be marked complete when its test(s) pass and `finish_feature` has been sent to create a per-feature commit.
- A plan is only complete when all related tests pass locally before submission.

## 7. Feature Completion Protocol (finish_feature)

### 7.1 Single Feature Cycle
Each execution cycle completes exactly one feature:
1. **Feature Selection**: Identify next Pending (`-`) feature from plan
2. **Status Update**: Change feature status from `-` to `~` (In Progress)
3. **Context Gathering**: Retrieve all required context using `retrieve_context_files`
4. **Implementation**: Complete the feature following its Action and Acceptance criteria
5. **Testing**: Create and validate tests for the feature
6. **Completion**: Update feature status to `+`, call `finish_feature`, then `finish`

### 7.2 Context Requirements Checklist
Before any feature implementation, verify:
- [ ] Current plan file read and understood
- [ ] Feature's Context files all retrieved
- [ ] Existing files to be modified inspected (not assumed)
- [ ] Related test files examined
- [ ] Dependencies satisfied

### 7.3 Finalization of the Task
- After all features send `finish_feature` and all tests pass, the agent:
  1) Updates `tasks/TASKS.md` marking the task as completed
  2) Calls `submit_for_review` to open a pull request
  3) Calls `finish` to end the cycle

## Summary of execution workflow:

1. Read the task specification from `tasks/TASKS.md`.
2. Create `tasks/{task_id}/plan_{task_id}.md` and enumerate features according to `docs/FEATURE_FORMAT.md`.
3. For each feature: gather MCC via `retrieve_context_files`, implement, write tests, run `run_tests`, then call `finish_feature` to commit the feature.
4. After all features pass tests: update `TASKS.md`, submit for review, and finish.

Context for implementation references: `scripts/run_tests.py`, `scripts/git_manager.py`, `scripts/run_local_agent.py`.