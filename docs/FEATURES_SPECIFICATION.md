# Features Specification

## 1. Purpose
This document defines what a Feature is within this project, how Features relate to Tasks, and enumerates the core Features of the agent. It adheres to the Specification Programming principles by focusing on WHAT each Feature must achieve. Any references to implementation map to the tool-based architecture and orchestration workflow, not to code-level details.

## 2. What is a Feature?
A Feature is a smaller, independently verifiable unit of work that contributes to completing a Task. Tasks express high-level goals; Features decompose those goals into testable increments while remaining implementation-agnostic.

- Scope: A Feature is narrow and testable; a Task is broader and strategic.
- Completion: A Task is complete only when all its Features have met their acceptance criteria.
- Traceability: Features are listed under their parent Task in tasks/TASKS.md and may reference this document for details.

## 3. Feature Format
A Feature follows a format closely aligned with the Task format but scoped to the parent Task. Feature IDs are local to the Task and start at 1.

Format inside a Task:

Feature N) STATUS Title
   Action: What needs to be done and why (WHAT, not code-level HOW)
   Acceptance: Objective, testable completion criteria
   Context: Reference files/specs that govern this feature
   Dependencies: [Optional] Other Features (by local number) or external Tasks
   Output: [Optional] Artifacts/changes produced
   Notes: [Optional] Additional relevant information

Status codes are the same as Tasks: + (Completed), ~ (In Progress), - (Pending), ? (Unknown), / (Blocked), = (Perpetual).

Numbering: Feature IDs are local to the Task (e.g., 1), 2), 3) ...). They do NOT need to be globally unique.

## 4. Relationship to Tasks
- Tasks define broader outcomes; Features define precise increments.
- A Task is complete if and only if all its Features are complete, unless explicitly marked as = (Perpetual) where completion is ongoing by design.
- Non-Redundancy Principle: Features should reference specifications (e.g., this file, TOOL_ARCHITECTURE.md) rather than duplicating them.

## 5. Success Criteria for Features
Each Feature MUST have acceptance criteria that are:
- Binary: The outcome is either achieved or not.
- Measurable: Can be verified through inspection or tests.
- Complete: Cover all critical aspects of the Feature’s behavior.

## 6. Constraints
- Features must not prescribe implementation details beyond referencing the orchestrator-tool contract and relevant specs.
- If a Feature introduces a paradigm shift that obsoletes prior documents, the task implementing that Feature must also remove/replace obsolete documents (Self-Cleaning Principle).

## 7. Edge Cases
- When context is ambiguous or involves architectural choices not specified, the Agent must use ask_question to pause and seek input.
- Features under Unknown tasks can be marked ? and should enumerate options and trade-offs.

## 8. Implementation Approach (High-Level HOW mapped to Architecture)
Implementation is executed by the Orchestrator as directed by the Agent through the tool-based contract (see docs/TOOL_ARCHITECTURE.md). The Agent expresses changes via JSON tool calls:
- write_file for content changes
- rename_files for safe moves/renames
- retrieve_context_files for reading context
- submit_for_review to create a PR
- ask_question for ambiguity
- finish to end the cycle

This mapping is the only acceptable mention of "how": Features may reference which tools or specs govern the change but avoid code details.

## 9. Canonical Agent Feature Catalog
This catalog defines the key Features the Agent must support. Tasks can reference these Features, and their acceptance criteria can be tested across implementations.

A) Planning and Workflow
1) Plan Generation
   Action: Produce a concise, human-readable plan that addresses the target Task and its Features before any tool calls.
   Acceptance:
   - Plan references the Task’s Action and Acceptance directly.
   - Plan lists a logical sequence that maps to the subsequent tool calls.
   - Plan ends with administrative steps: update TASKS.md, submit_for_review, finish.
   Context: docs/PLAN_SPECIFICATION.md, docs/TOOL_ARCHITECTURE.md

2) Mandatory Workflow Compliance
   Action: Ensure every successful completion sequence adheres to the mandatory workflow.
   Acceptance:
   - write_file calls include all necessary content updates, including TASKS.md status updates.
   - submit_for_review is called with correct task_id and task_title.
   - finish is called after submit_for_review.
   Context: docs/TOOL_ARCHITECTURE.md

B) Context and Safety
3) Context Gathering
   Action: Gather and use the project context files listed by the Orchestrator.
   Acceptance:
   - The plan uses only allowed context files or retrieve_context_files.
   - No attempt to access files outside provided context.
   Context: scripts/run_local_agent.py (context list), docs/FILE_ORGANISATION.md

4) Ambiguity Handling
   Action: Halt and ask a clear question when faced with under-specified decisions.
   Acceptance:
   - ask_question is used only for genuine ambiguities.
   - Question is concise and actionable.
   Context: docs/AGENT_PRINCIPLES.md

C) File Operations
5) Content Authoring
   Action: Create or update Markdown/spec files in compliance with specs.
   Acceptance:
   - Content adheres to specification style (WHAT, not HOW; success criteria are verifiable).
   - Files are placed according to FILE_ORGANISATION.md.
   Context: docs/SPECIFICATION_GUIDE.md, docs/FILE_ORGANISATION.md

6) Safe Renames/Moves
   Action: Perform intra-repo renames/moves safely.
   Acceptance:
   - rename_files returns ok=true with no errors in dry-run mode, then in execution.
   - No path escapes beyond repo root.
   Context: docs/TOOL_ARCHITECTURE.md

D) Git and Submission
7) Standardized Submission
   Action: Submit work for review via standardized commit and PR process.
   Acceptance:
   - submit_for_review succeeds with a PR created.
   - Commit message includes Task ID and Title per the orchestrator standard.
   Context: scripts/run_local_agent.py

E) Execution Modes
8) Single vs Continuous Mode Compatibility
   Action: Plans are valid in both modes.
   Acceptance:
   - Plans end with finish, allowing continuous mode to proceed correctly.
   - No reliance on multi-turn memory outside the plan/tool_calls.
   Context: docs/TOOL_ARCHITECTURE.md

F) Error Handling and Robustness
9) Robust JSON Contract
   Action: Produce a single valid JSON object with required keys and structure.
   Acceptance:
   - JSON parses successfully without code fences unless explicitly allowed.
   - All tool calls use the arguments key for parameters.
   Context: docs/TOOL_ARCHITECTURE.md

10) Validation and Idempotence
   Action: Author changes so that re-running the plan does not corrupt files.
   Acceptance:
   - Re-running does not introduce duplicate sections or malformed content.
   Context: docs/SPECIFICATION_GUIDE.md

## 10. Governance
- This catalog may evolve via future Tasks. Changes must update this file and corresponding Features in tasks/TASKS.md.
- When a whole paradigm is replaced, the responsible task must remove obsolete references (Self-Cleaning Principle).
