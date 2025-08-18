# Feature Definitions

## 1. Purpose
This document defines the agent's features and how they are to be executed within the Specification Programming framework. It provides a unified, testable description of the agent's capabilities so multiple implementations produce functionally identical outcomes.

## 2. Definitions
- Feature: A self-contained capability that contributes to completing tasks as defined in tasks/TASKS.md.
- Sub-feature: A smaller capability that composes a feature.
- Dependency: Another feature or external requirement that must exist or execute before this feature.
- Status: One of Planned, Implemented, or Deprecated (used for roadmap and evolution).

## 3. Feature Specification Template
Each feature should be described with the following fields:
- Name
- Problem Statement
- Inputs
- Outputs
- Constraints
- Success Criteria
- Edge Cases
- Dependencies
- Implementation Notes (non-binding guidance)

## 4. Feature Catalog
The following features define the current agent’s expected behavior and boundaries.

### F1) Task Selection and Eligibility
- Problem Statement: Determine the next eligible task to work on from tasks/TASKS.md.
- Inputs:
  - tasks/TASKS.md content
- Outputs:
  - Selected task id (integer)
  - Selected task title (string)
  - Selected task status before change (one of +, ~, -, ?, /, =)
- Constraints:
  - Prefer the earliest task that is Pending (-). If none exist, the earliest Unknown (?) is eligible and should be resolved within the same cycle if feasible.
  - Respect dependencies when explicitly listed; if ambiguous, escalate with ask_question.
  - Follow the Non-Redundancy and Sequential Knowledge principles.
- Success Criteria:
  1) The selected task is either Pending (-) or Unknown (?) and is the earliest such task in the list not blocked by dependencies.
  2) If selection is ambiguous due to conflicting dependencies or unclear order, ask_question is called instead of proceeding.
- Edge Cases:
  - No eligible tasks found: finish with reason "HALT: No eligible tasks found." per TOOL_ARCHITECTURE.
  - Malformed tasks file: ask_question with clear error.
- Dependencies: None.
- Implementation Notes:
  - Parsing is logical; exact parsing code is not constrained by this spec as long as outputs meet the criteria.

### F2) Plan Creation and Contract Compliance
- Problem Statement: Produce a high-level plan and a list of tool calls in a single JSON object compliant with TOOL_ARCHITECTURE.md and PLAN_SPECIFICATION.md.
- Inputs:
  - Selected task details
  - docs/TOOL_ARCHITECTURE.md
  - docs/PLAN_SPECIFICATION.md
- Outputs:
  - JSON object with keys: plan (string) and tool_calls (array)
- Constraints:
  - JSON only, no prose outside the object.
  - Must include write_file for all new/changed files, write_file to update tasks/TASKS.md, submit_for_review, and finish.
- Success Criteria:
  1) The response is valid JSON with plan and tool_calls.
  2) The final tool_calls include, in order: write_file changes, write_file TASKS.md update, submit_for_review, finish.
  3) No extraneous tool calls are included.
- Edge Cases:
  - Large content: tool_calls must still be valid and atomic; if not possible, ask_question.
- Dependencies: F1.
- Implementation Notes:
  - Keep the plan concise and map steps to tool calls.

### F3) Documentation Authoring
- Problem Statement: Create or modify documentation files to satisfy a task’s acceptance criteria while adhering to SPECIFICATION_GUIDE.md.
- Inputs:
  - docs/SPECIFICATION_GUIDE.md
  - Task acceptance requirements
- Outputs:
  - Markdown content for the specified file(s)
- Constraints:
  - Documentation must focus on WHAT, not implementation-specific HOW unless the task explicitly calls for implementation guidance.
  - Use clear, testable acceptance language where appropriate.
- Success Criteria:
  1) The new/updated document addresses the task’s acceptance criteria fully.
  2) Content aligns with SPECIFICATION_GUIDE.md (problem/inputs/outputs/constraints/success criteria/edge cases where applicable).
- Edge Cases:
  - Conflicting guidance across documents: ask_question with proposed resolution.
- Dependencies: None.
- Implementation Notes:
  - Prefer consistent section ordering and headings across docs.

### F4) File Authoring via write_file
- Problem Statement: Materialize changes to the repository as files.
- Inputs:
  - Target path (string)
  - Content (string)
- Outputs:
  - File written at path with the exact content
- Constraints:
  - Paths must remain inside the repository.
  - Directories must be created as needed.
- Success Criteria:
  1) File exists with exact content as provided.
  2) Re-running the same action is idempotent (results in no functional change).
- Edge Cases:
  - Overwriting existing content: allowed; content must match new version.
- Dependencies: None.
- Implementation Notes:
  - Use docs/ for specifications, scripts/ for executables, per FILE_ORGANISATION.md.

### F5) Task Status Update Protocol
- Problem Statement: Update tasks/TASKS.md to reflect the new status after performing work.
- Inputs:
  - Current tasks/TASKS.md
  - Completed task id and title
- Outputs:
  - Updated tasks/TASKS.md with correct status symbol and preserved formatting
- Constraints:
  - For Unknown (?) tasks resolved by producing the required artifact and selecting a definitive approach, set to Completed (+). If the unknown was only clarified and requires further work, set to Pending (-) with rewritten Action/Acceptance accordingly.
  - Preserve surrounding content and other tasks unmodified.
- Success Criteria:
  1) The target task’s status symbol reflects the actual outcome (+ if completed as accepted; - if now concretized but still to be done).
  2) No other tasks are altered unintentionally.
- Edge Cases:
  - If acceptance cannot be objectively verified, ask_question.
- Dependencies: F1, F4.
- Implementation Notes:
  - Maintain consistency with TASK_FORMAT.md.

### F6) Review Submission Protocol
- Problem Statement: Package and submit changes for human review.
- Inputs:
  - task_id (int)
  - task_title (string)
- Outputs:
  - PR created with standardized commit title and body
- Constraints:
  - Must run after all write_file operations are completed.
- Success Criteria:
  1) submit_for_review is called exactly once with the correct task_id and task_title.
- Edge Cases:
  - If submission fails per orchestrator message, the tool returns failure text; do not retry in the same cycle.
- Dependencies: F4, F5.
- Implementation Notes:
  - Follow the commit and PR conventions in the orchestrator.

### F7) Safety and Escalation via ask_question
- Problem Statement: Halt execution and request human input when an ambiguity or major unspecified decision arises.
- Inputs:
  - question_text (string)
- Outputs:
  - A halt with a clear question to the user
- Constraints:
  - Only use when necessary.
- Success Criteria:
  1) When used, the question concisely describes the decision needed and the options.
- Edge Cases:
  - Non-blocking uncertainties should not trigger escalation.
- Dependencies: None.
- Implementation Notes:
  - Provide actionable multiple-choice options when possible.

### F8) Safe Rename/Move Operations
- Problem Statement: Perform repository-safe renames and moves.
- Inputs:
  - operations: list of {from_path, to_path}
  - overwrite (bool), dry_run (bool)
- Outputs:
  - JSON result summary from rename_files
- Constraints:
  - Operations must remain within the repository.
- Success Criteria:
  1) rename_files returns ok=true for intended moves or provides explicit error messages.
- Edge Cases:
  - Existing destination without overwrite: should be skipped with explicit message.
- Dependencies: None.
- Implementation Notes:
  - Prefer dry_run first for critical restructures.

### F9) Context Retrieval for Grounding
- Problem Statement: Retrieve repository files as grounding context when needed.
- Inputs:
  - paths (list[string])
- Outputs:
  - JSON map of {path: content or error}
- Constraints:
  - Use sparingly; the orchestrator already passes common context.
- Success Criteria:
  1) Retrieved content matches actual file state.
- Edge Cases:
  - Missing files return clear error strings without failing the cycle.
- Dependencies: None.
- Implementation Notes:
  - Use when a task references files not included in the default context bundle.

### F10) Continuous Execution Lifecycle Control
- Problem Statement: Conclude cycles appropriately in single or continuous modes.
- Inputs:
  - reason (string) for finish
- Outputs:
  - Cycle termination signal
- Constraints:
  - Use finish after submit_for_review, or with reason "HALT: No eligible tasks found." when applicable.
- Success Criteria:
  1) finish is called exactly once per cycle.
- Edge Cases:
  - If ask_question was called, do not call finish.
- Dependencies: F2, F6.
- Implementation Notes:
  - Provide concise, informative finish reasons.

### F11) Feature-Driven Task Decomposition
- Problem Statement: Break complex tasks into features and sub-features while preserving the overarching task context.
- Inputs:
  - Task description and acceptance criteria
- Outputs:
  - A feature list that maps to the task’s acceptance criteria
- Constraints:
  - Do not proliferate separate tasks when features suffice; maintain context within the task.
- Success Criteria:
  1) Each feature is independently verifiable and collectively sufficient to fulfill the task.
- Edge Cases:
  - Cross-feature dependencies must be explicit; if not resolvable, ask_question.
- Dependencies: F3, F2.
- Implementation Notes:
  - Optionally store detailed per-task plans in plans/ per FILE_ORGANISATION.md.

### F12) Testing Readiness
- Problem Statement: Ensure outputs are structured so future automated tests (TESTING.md) can validate them.
- Inputs:
  - Current specifications
- Outputs:
  - Documents and artifacts with clear, objective success criteria
- Constraints:
  - Success criteria must be binary, measurable, and complete.
- Success Criteria:
  1) New/updated specs include explicit Success Criteria sections that can be tested.
- Edge Cases:
  - Legacy documents without criteria should be flagged for future improvement (not blocking current tasks).
- Dependencies: F3.
- Implementation Notes:
  - Align with SPECIFICATION_GUIDE.md best practices.

## 5. Compliance and Evolution
- This catalog is living; when a new paradigm supersedes an existing one, update this file in the same task that introduces the change (Self-Cleaning Principle).
- All new features must be added here with full specification before implementation tasks proceed.
