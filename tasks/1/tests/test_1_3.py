import sys
import os
import json
import importlib.util

def run():
    # Acceptance Criterion 1: `docs/tasks/task_example.json` exists.
    file_path = "docs/tasks/task_example.json"
    if not os.path.exists(file_path):
        print(f"FAIL: {file_path} does not exist.")
        sys.exit(1)

    # Acceptance Criterion 2: The file contains a valid JSON object.
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"FAIL: {file_path} is not a valid JSON file. Error: {e}")
        sys.exit(1)

    # Acceptance Criterion 3: The JSON object structure conforms to the `Task` schema.
    try:
        spec = importlib.util.spec_from_file_location("task_format", "docs/tasks/task_format.py")
        task_format = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(task_format)
        Task = task_format.Task
    except Exception as e:
        print(f"FAIL: Could not import Task schema from docs/tasks/task_format.py. Error: {e}")
        sys.exit(1)
    
    # Task has no optional fields, so we check all its annotations.
    required_task_fields = set(Task.__annotations__.keys())
    if not required_task_fields.issubset(data.keys()):
        missing = required_task_fields - set(data.keys())
        print(f"FAIL: {file_path} is missing required Task fields: {missing}")
        sys.exit(1)

    print("PASS: docs/tasks/task_example.json exists, is valid JSON, and conforms to the basic Task schema.")
    sys.exit(0)

if __name__ == "__main__":
    run()
