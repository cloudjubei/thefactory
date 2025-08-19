# Problem Statement
<Describe the core problem and motivation in 2-5 sentences.>

Example:
- We need a single entry-point specification file that guides contributors and tools.

# Inputs and Outputs
<Enumerate all inputs and outputs with types and examples.>

Inputs:
- Task description (markdown)
- Repo context files (paths)

Outputs:
- Created/updated documentation files
- Passing tests under tasks/{task_id}/tests/

# Constraints
<List technical, operational, and organizational constraints.>

- Use only standard library for tests
- Files must be UTF-8 encoded
- Deterministic test outcomes (no network calls)

# Success Criteria
<Define objective, verifiable success conditions.>

- Required files exist at exact paths
- Files contain required headings/phrases
- run_tests exits with code 0

# Edge Cases
<List edge cases and expected handling.>

- Missing directories: create them as needed
- Pre-existing files: update content idempotently
- Extra sections: allowed if core headings remain intact

# Examples
<Provide concrete examples of correct outputs.>

- Example: SPECIFICATION_GUIDE.md includes headings: Problem Statement, Inputs and Outputs, Constraints, Success Criteria, Edge Cases, Examples.
- Example: TEMPLATE.md includes the same headings with placeholders and example snippets.