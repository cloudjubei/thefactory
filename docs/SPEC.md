Reference: docs/SPECIFICATION_GUIDE.md

# Problem Statement
This project defines a specification-driven, tool-executing AI agent system. The agent produces plans and atomic feature changes via a fixed JSON contract and uses a safe tool interface to manipulate repository content. The core problem is enabling reliable, auditable progress on tasks through well-structured specifications, plans, and per-feature commits with passing tests.

# Inputs and Outputs
- Inputs:
  - Task descriptions in tasks/TASKS.md
  - Task plans at tasks/{task_id}/plan_{task_id}.md following PLAN_SPECIFICATION and FEATURE_FORMAT
  - Core specifications and guides under docs/ (PLAN_SPECIFICATION, TESTING, FEATURE_FORMAT, TOOL_ARCHITECTURE)
  - Existing repository files to be read or modified by features
- Outputs:
  - Updated or newly created files per feature acceptance criteria
  - Tests under tasks/{task_id}/tests/ that encode acceptance criteria
  - Per-feature commits via finish_feature; final PR via submit_for_review once a task is fully completed

# Constraints
- All changes must be performed via SAFE tools and the JSON response contract
- One cycle completes exactly one feature; minimize changes and avoid rewriting files unnecessarily
- Tests must be deterministic and pass before marking a feature complete
- docs/SPEC.md adheres to docs/SPECIFICATION_GUIDE.md structure
- The orchestrator enforces tool usage and isolates feature commits

# Success Criteria
- Features are implemented atomically and match their acceptance criteria
- Corresponding tests exist (as dedicated features where applicable) and pass via run_tests
- Plans and statuses are kept up-to-date; per-feature commits are created using finish_feature
- The specification documents remain consistent, discoverable, and reference the correct guides

# Edge Cases
- Missing or ambiguous context: agent must retrieve required files or ask questions before proceeding
- Legacy sections in docs that conflict with the current guide: resolve by aligning to the guide without introducing extraneous top-level sections
- Tests that depend on environment or external services: must be avoided; keep deterministic and local

# Examples
- Updating docs/SPEC.md to include required sections and a top reference to docs/SPECIFICATION_GUIDE.md
- Creating template and guide files as separate features, with separate test features that verify presence of required headings
- Implementing a file change feature followed by a test feature that checks for exact headings and file paths
