# Agent Testing Specification

## 1) Purpose and Scope
Testing encodes acceptance criteria into deterministic, executable checks so feature completion is objective and reproducible. This specification defines where tests live, how they are named, how they are structured, how to write them from acceptance criteria, how to run them, and how the agent uses the testing tools. It applies to all tasks and features in this repository.

## 2) Test Locations and Naming Conventions
- Location per task: tests for a given task reside under tasks/{task_id}/tests/.
- File naming per feature: test_{task_id}_{feature_number}.py
  - Example: Task 15, Feature 3 -> tasks/15/tests/test_15_3.py
- One-to-one mapping: each feature that produces tangible output has at least one corresponding test file that verifies its acceptance criteria.
- Cohesion: tests must only assert the acceptance criteria for their corresponding feature, avoiding cross-feature coupling.

## 3) Test Structure and Utilities
- Simplicity: tests are plain Python scripts using only the standard library (os, sys, json, etc.). Avoid frameworks unless explicitly required by a task.
- Determinism: tests must not depend on network calls or non-deterministic inputs. Use fixed strings and file assertions.
- Assertions: prefer explicit checks with clear PASS/FAIL messages and exit codes (0 success, 1 failure).
- Utilities: if simple helper logic is needed, keep it within the test file or a dedicated helper in the same task folder to avoid global coupling. Introduce shared utilities only when clearly warranted by multiple tasks and document them.

## 4) Writing Acceptance Tests
- Start from the feature's Acceptance section in the task plan and translate each criterion into a concrete assertion.
- Typical checks include:
  - File existence: verify required files were created/updated at the correct paths.
  - Content validation: check presence of required headings, phrases, or structural markers.
  - Structure: ensure directory layout and naming conventions match the spec.
- One test per feature: encode all acceptance points for that feature in its corresponding test file.
- Independence: tests should set up only what they need and make no assumptions about other features beyond documented dependencies.

## 5) Running Tests
- Tool: use the run_tests tool exposed by the orchestrator. It invokes scripts/run_tests.py.
- Expected outputs: the tool returns a JSON-like result with fields such as ok, exit_code, stdout, stderr, and optionally passed/total.
- Local behavior: tests are executed from the repository root; relative paths in tests should be rooted appropriately.
- Passing rule: a test must exit with code 0 and print a clear PASS message for success.

## 6) CI/Automation Expectations
- Gating: a feature cannot be marked complete until its corresponding test passes.
- Per-feature commits: upon completing and validating a feature, the agent must call finish_feature to create an isolated commit for that feature.
- Task completion: a task is only submitted for review when all features and their tests pass across the full suite.
- Stability: tests should produce identical results across environments given the same repo state.

## 7) Tool Usage
- run_tests: the agent calls the run_tests tool to execute the suite and uses the returned result to decide whether to proceed or fix failures.
- finish_feature: after a feature's test passes, the agent calls finish_feature to create a per-feature commit (distinct from the final submit_for_review call used to open a PR after all features are done).

## 8) Examples
Minimal example mapping a feature to a test:

Feature (Task 4, Feature 1): "Create a specification template at docs/TEMPLATE.md with required headings."

Example test file: tasks/4/tests/test_4_1.py

```python
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

## 9) References
- docs/PLAN_SPECIFICATION.md
- docs/TASK_FORMAT.md
- docs/TOOL_ARCHITECTURE.md
