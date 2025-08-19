import os
import sys

def run():
    """
    Tests for Feature 13.1: Define Task Schema in Python.
    Acceptance Criteria:
     - `docs/tasks/task_format.py` exists.
     - The file defines Python types for `Task`, `Feature`.
     - The types cover all fields currently used.
    """
    file_path = "docs/tasks/task_format.py"
    print(f"--- Test for Feature 13.1: Checking {file_path} ---")

    # 1. Check if file exists
    if not os.path.exists(file_path):
        print(f"FAIL: File '{file_path}' does not exist.")
        sys.exit(1)
    
    print(f"PASS: File '{file_path}' exists.")

    # 2. Check for required type definitions
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    required_definitions = [
        "class Feature(TypedDict):",
        "class Task(TypedDict):",
        'Status = Literal["+", "~", "-", "?", "/", "="]'
    ]
    
    missing_definitions = []
    for definition in required_definitions:
        if definition not in content:
            missing_definitions.append(definition)

    if missing_definitions:
        print(f"FAIL: File '{file_path}' is missing the following definitions: {', '.join(missing_definitions)}")
        sys.exit(1)

    print(f"PASS: File '{file_path}' contains the required type definitions.")

    # 3. Check for key fields in Task and Feature
    feature_fields = ['feature_id: int', 'status: Status', 'title: str', 'action: str', 'acceptance: str']
    task_fields = ['task_id: int', 'status: Status', 'title: str', 'action: str', 'acceptance: str', 'features: List[Feature]']
    
    missing_fields = []
    for field in feature_fields:
        if field not in content:
            missing_fields.append(f"Feature.{field}")
    for field in task_fields:
        if field not in content:
            missing_fields.append(f"Task.{field}")
    
    if missing_fields:
        print(f"FAIL: File '{file_path}' is missing the following field definitions: {', '.join(missing_fields)}")
        sys.exit(1)

    print(f"PASS: File '{file_path}' contains the expected fields for Task and Feature.")
    print("--- Test for Feature 13.1 Succeeded ---")
    sys.exit(0)

if __name__ == "__main__":
    run()
