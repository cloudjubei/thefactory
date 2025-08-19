# Plan for Task 6: Define Core Agent Terminology and Principles

## Intent
Establish core principles, terminology, and tool-based architecture for the Agent, and ensure the plan encodes per-feature testing and completion flow per the Plan Specification.

## Context
- Specs: docs/PLAN_SPECIFICATION.md, docs/FEATURE_FORMAT.md, docs/TASK_FORMAT.md, docs/TOOL_ARCHITECTURE.md
- Orchestrator: scripts/run_local_agent.py
- Task list: tasks/TASKS.md

## Features
6.1) + Create the tools guide
   Action: Specify the JSON contract, tools, and execution modes.
   Acceptance: docs/TOOL_ARCHITECTURE.md exists with all sections and tool definitions.
   Context: docs/PLAN_SPECIFICATION.md, docs/FEATURE_FORMAT.md, docs/TASK_FORMAT.md
   Output: docs/TOOL_ARCHITECTURE.md

6.2) + Create the principles guide
   Action: Define Agent vs Orchestrator and core principles.
   Acceptance: docs/AGENT_PRINCIPLES.md exists and contains required definitions referencing the tools guide.
   Context: docs/PLAN_SPECIFICATION.md, docs/TOOL_ARCHITECTURE.md, docs/FEATURE_FORMAT.md
   Dependencies: 6.1
   Output: docs/AGENT_PRINCIPLES.md

6.3) + Document agent personas
   Action: Author docs/AGENT_PERSONAS.md describing Manager, Planner, Tester, Developer personas, including objectives, constraints, prompts, minimal context, and instructions to run each via scripts/run_local_agent.py.
   Acceptance: docs/AGENT_PERSONAS.md exists with clear definitions and run examples; references docs/TOOL_ARCHITECTURE.md and docs/AGENT_PRINCIPLES.md.
   Context: docs/PLAN_SPECIFICATION.md, docs/TOOL_ARCHITECTURE.md, scripts/run_local_agent.py, docs/FEATURE_FORMAT.md
   Output: docs/AGENT_PERSONAS.md

6.4) + Deprecate tasks 7 and 10 (merged into Task 6)
   Action: Update tasks/TASKS.md to mark tasks 7 (Agent Orchestrator) and 10 (Agent personas) as = Deprecated with notes referencing Task 6.
   Acceptance: tasks/TASKS.md shows tasks 7 and 10 as deprecated and pointing to Task 6 and relevant docs.
   Context: tasks/TASKS.md, docs/TASK_FORMAT.md
   Output: tasks/TASKS.md

6.5) + Tests for tools guide (6.1)
   Action: Create a deterministic test that verifies docs/TOOL_ARCHITECTURE.md exists and includes key sections.
   Acceptance:
   - tasks/6/tests/test_6_5.py exists
   - The test verifies presence of headings/phrases: "Tool-Using Agent Architecture", "Available Tools", "Mandatory Task Completion Workflow"
   - The test prints PASS/FAIL and exits 0/1 accordingly
   Context: docs/PLAN_SPECIFICATION.md (Section 6: Testing), docs/TOOL_ARCHITECTURE.md, tasks/6/plan_6.md
   Dependencies: 6.1
   Output: tasks/6/tests/test_6_5.py

6.6) - Tests for principles guide (6.2)
   Action: Create a deterministic test that verifies docs/AGENT_PRINCIPLES.md exists and includes key sections.
   Acceptance:
   - tasks/6/tests/test_6_6.py exists
   - The test verifies presence of phrases/headings: "Agent vs Orchestrator", "Core Principles"
   - The test prints PASS/FAIL and exits 0/1 accordingly
   Context: docs/PLAN_SPECIFICATION.md (Section 6: Testing), docs/AGENT_PRINCIPLES.md, tasks/6/plan_6.md
   Dependencies: 6.2
   Output: tasks/6/tests/test_6_6.py

6.7) - Tests for agent personas (6.3)
   Action: Create a deterministic test that verifies docs/AGENT_PERSONAS.md exists and enumerates all personas and run examples.
   Acceptance:
   - tasks/6/tests/test_6_7.py exists
   - The test verifies presence of "Manager", "Planner", "Tester", "Developer" and a section mentioning scripts/run_local_agent.py run examples
   - The test prints PASS/FAIL and exits 0/1 accordingly
   Context: docs/PLAN_SPECIFICATION.md (Section 6: Testing), docs/AGENT_PERSONAS.md, scripts/run_local_agent.py, tasks/6/plan_6.md
   Dependencies: 6.3
   Output: tasks/6/tests/test_6_7.py

6.8) - Tests for deprecation updates (6.4)
   Action: Create a deterministic test that verifies tasks 7 and 10 are marked as = Deprecated in tasks/TASKS.md and reference Task 6.
   Acceptance:
   - tasks/6/tests/test_6_8.py exists
   - The test verifies in tasks/TASKS.md: entries "7) =" and "10) =" and that their notes reference Task 6
   - The test prints PASS/FAIL and exits 0/1 accordingly
   Context: docs/PLAN_SPECIFICATION.md (Section 6: Testing), tasks/TASKS.md, tasks/6/plan_6.md
   Dependencies: 6.4
   Output: tasks/6/tests/test_6_8.py

## Execution Steps
For each feature in order:
1) Gather Minimum Cohesive Context (MCC) using retrieve_context_files and implement the feature changes
2) Create test(s) that verify the feature's acceptance criteria under tasks/6/tests/
3) Run tests using the run_tests tool and ensure they pass
4) Call finish_feature with a descriptive message (e.g., "Feature 6.{n} complete: {Title}") to create a per-feature commit

After all features are completed:
5) Run run_tests again and ensure the full suite passes
6) Update tasks/TASKS.md with the status change for this task if needed
7) Submit for review (open PR)
8) Finish
