# Feature Format

## Purpose
Features are atomic, testable pieces of work that collectively satisfy a task. They define WHAT must be delivered without prescribing HOW to implement it, and they reference the project specifications rather than duplicating them.

## Where Features Live
- Each task has a dedicated plan file located at `tasks/{task_id}/plan_{task_id}.md`.
- Features for that task are enumerated in that plan file.

## Format
```
ID) STATUS Title
   Action: What needs to be done and why
   Acceptance: Objective, testable criteria to verify completion
   Context: [Optional] Specification files (and sections) this feature relies on
   Dependencies: [Optional] Other features (e.g., 13.1) or tasks (by ID) that must be done first
   Output: [Optional] Artifacts this feature produces or changes
   Notes: [Optional] Additional clarifications
   Rejection: [Optional] Information about why this feature is currently being rejected
```

## Field Definitions

### ID
- Use `{task_id}.{n}` where `n` is a positive integer starting at 1 and `task_id` is the ID of the parent task.
- All the features under one task share an incrementing counter.
- Examples: `7.1`, `7.2`, `7.3`.

### Title
A succinct higher level name for the feature

### Status
- `+` Completed - a feature that is done
- `~` In Progress - a feature that is being worked on
- `-` Pending - a feature that requires work
- `?` Unknown - a feature that requires defining options with pros/cons; after choosing, rewrite as Pending
- `/` Blocked - a feature started but cannot proceed due to external factors
- `=` Perpetual - a feature that is always Pending but low priority, no end date

### Acceptance
Concrete, testable conditions that define feature completion. These should be:
- Verifiable: Can be checked objectively
- Specific: No room for interpretation
- Complete: When all criteria are met, the feature is done

Good acceptance criteria answers: "What must be achieved for this feature to be finished? How can this be verified?"

### Context
List of files that contain any relevant information needed for completing the feature. Format: comma-and-space separated list of filenames, optionally with sections.
Example: `docs/TOOL_ARCHITECTURE.md`, `docs/AGENT_PRINCIPLES.md`

### Dependencies
Lists feature IDs that must be completed before this feature can begin. Format: comma-and-space separated list of IDs.
Example: `7.5, 7.9`

### Output
Describes what will be created or changed. Could be files, documentation, code, or process changes.

### Notes
Any extra notes about the feature that explain reasoning or give extra hints about how to accomplish the feature. Especially useful for `Unknown` features that usually require a discussion.

### Rejection
Concrete reason that defines why the feature is not accepted.
If the reason introduces new spec that isn't already covered elsewhere, add it to the spec.

## Examples

### Completed Feature
```
13.1) + Create the Feature Format specification
   Action: Provide a dedicated specification for describing features so plans can reference and structure them consistently.
   Acceptance:
   - docs/FEATURE_FORMAT.md exists
   - The document includes Purpose, Where Features Live, Numbering, Format, Field Definitions, and Examples
   - The format references project specs and avoids duplicating implementation details
   Context: docs/SPECIFICATION_GUIDE.md, docs/TASK_FORMAT.md
   Output: docs/FEATURE_FORMAT.md
   Notes: This enables consistent plan authoring across tasks.
```

### Pending Feature
```
7.10) - Retrieve context files tool
   Action: Implement a tool that returns the contents of specified files to the agent.
   Acceptance:
   - scripts/tools/retrieve_context_files.py exists
   - Function signature: retrieve_context_files_tool(base_dir: str, paths: list[str]) -> dict
   - Returns a dict with keys: ok (bool), files (list of {path, content}), errors (list of {path, error})
   Context: docs/TOOL_ARCHITECTURE.md
   Output: scripts/tools/retrieve_context_files.py
   Notes: This enables the agent to fetch additional context mid-execution.
```

### In-Progress Feature
```
7.6) ~ Orchestrator can parse and call tools
   Action: Add JSON parsing and dynamic dispatch to execute tool calls defined by the agent.
   Acceptance:
   - A valid agent JSON response results in the corresponding tool being executed
   - Unknown tool names are logged and skipped without crashing
   - Errors during tool execution are surfaced and halt the cycle
   Context: docs/TOOL_ARCHITECTURE.md, scripts/run_local_agent.py
   Dependencies: 7.5
   Notes: Partial implementation landed; error handling still being refined.
```

### Unknown Feature
```
19.2) ? Define test harness format
   Action: Decide on the structure for test scenario definition files (YAML vs JSON vs Python DSL) to validate agent behavior.
   Acceptance:
   - A decision document exists with the chosen format and rationale
   - The feature is rewritten as Pending with concrete implementation steps
   Context: docs/TESTING.md (to be created)
   Notes:
   - Options:
     - YAML: human-friendly, widely used
       Pros: readable, comments; Cons: indentation pitfalls
     - JSON: strict and simple tooling
       Pros: ubiquitous; Cons: less readable, no comments
     - Python DSL: maximal flexibility
       Pros: powerful; Cons: execution risk, complexity
   Output: docs/TEST_HARNESS_FORMAT_DECISION.md
```

### Blocked Feature
```
18.3) / Provision AWS credentials for CI
   Action: Set up OIDC role and permissions to allow GitHub Actions to deploy infrastructure.
   Acceptance:
   - Role ARN documented and verified
   - GitHub workflow uses role to perform a no-op AWS call
   Context: docs/RUNNING_ON_CLOUD.md
   Dependencies: 18.1 (AWS account setup)
   Notes: Blocked pending org approval for AWS account access.
```

### Perpetual Feature
```
8.5) = Documentation linting
   Action: Periodically lint and normalize markdown across the repo (headings, trailing spaces, link checks).
   Acceptance:
   - Lint script exists and can be run on demand
   - No broken internal links in docs/
   Output: scripts/lint_docs.py
   Notes: Ongoing maintenance; low priority.
```

### Pending Feature that serves as a group container for other features
```
20.0) - Local app MVP
   Action: Parent feature to group the MVP capabilities for the local project management app.
   Acceptance:
   - This feature is considered complete when 20.1, 20.2, and 20.3 are completed
   Dependencies: 20.1, 20.2, 20.3
   Notes: No direct output; serves as a container.
```
