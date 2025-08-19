# Agent Testing Specification

## 1. Philosophy
Testing is a critical part of the agent's development process. It ensures that features and tasks are completed correctly, and that the agent's behavior is verifiable and reproducible. Every feature should be testable, and the tests serve as a concrete definition of "done."

Tests are not a separate, optional step; they are an integral part of the feature delivery process. The acceptance criteria of a feature directly inform the creation of its tests.

## 2. Test Location
- All tests for a specific task reside within that task's directory.
- The standard location for tests is `tasks/{task_id}/tests/`.
- For a feature `X.Y`, its test might be located at `tasks/X/tests/test_feature_Y.py`.

This co-location ensures that tests are tightly coupled with the task and features they validate.

## 3. Test Structure
Tests should be simple, executable scripts (e.g., Python scripts using the standard library) that verify the acceptance criteria of a feature. They should be self-contained and not require complex frameworks unless absolutely necessary.

A typical test script for a feature that creates a file might:
1. Check for the existence of the output file(s).
2. Read the content of the file(s).
3. Assert that the content matches the expected structure or contains specific key phrases.
4. Exit with a status code of `0` for success and `1` for failure.

### Example Test (`tasks/4/tests/test_feature_1.py`)

Suppose Task 4, Feature 1 was "Create a specification template."

```python
# tasks/4/tests/test_feature_1.py
import os
import sys

def run_test():
    """
    Tests that TEMPLATE.md was created correctly.
    - Checks if docs/TEMPLATE.md exists.
    - Checks if it contains required sections.
    """
    template_path = "docs/TEMPLATE.md"
    
    # 1. Check for file existence
    if not os.path.exists(template_path):
        print(f"FAIL: {template_path} does not exist.")
        sys.exit(1)
        
    # 2. Check for content
    with open(template_path, "r") as f:
        content = f.read()
    
    required_sections = [
        "# Problem Statement",
        "# Inputs and Outputs",
        "# Constraints",
        "# Success Criteria",
        "# Edge Cases"
    ]
    
    missing_sections = []
    for section in required_sections:
        if section not in content:
            missing_sections.append(section)
            
    if missing_sections:
        print(f"FAIL: {template_path} is missing sections: {', '.join(missing_sections)}")
        sys.exit(1)
        
    print("PASS: docs/TEMPLATE.md exists and contains all required sections.")
    sys.exit(0)

if __name__ == "__main__":
    run_test()
```

## 4. The Testing Workflow
The requirement to create and pass tests is integrated into the planning and execution process. See `docs/PLAN_SPECIFICATION.md` for how this is formally included in the agent's workflow.

### 4.1 Within Feature Execution
Testing is integrated into each feature cycle:
1. **Implementation**: Complete the feature's primary work
2. **Test Creation**: Write test file at `tasks/{task_id}/tests/test_{task_id}_{feature_number}.py`
3. **Test Validation**: Run `run_tests` tool to verify test passes
4. **Feature Completion**: Only mark feature complete (`+`) when test passes

### 4.2 Test File Naming Convention
- Format: `test_{task_id}_{feature_number}.py`
- Example: Feature 15.3 → `tasks/15/tests/test_15_3.py`
- Location: Always in `tasks/{task_id}/tests/` directory

### 4.3 Test Failure Protocol
If tests fail:
1. **Do NOT mark feature complete**
2. Fix the implementation or test as needed
3. Re-run `run_tests` until passing
4. Only then update feature status to `+`
