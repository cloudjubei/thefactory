import sys
import os
import importlib.util

def run():
    # Acceptance Criterion 1: `docs/tasks/task_format.py` exists.
    file_path = "docs/tasks/task_format.py"
    if not os.path.exists(file_path):
        print(f"FAIL: {file_path} does not exist.")
        sys.exit(1)

    # Acceptance Criterion 2: The file defines Python TypedDicts for `Task` and `Feature`.
    try:
        spec = importlib.util.spec_from_file_location("task_format", file_path)
        task_format = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(task_format)
    except Exception as e:
        print(f"FAIL: Could not import {file_path}. Error: {e}")
        sys.exit(1)

    if not hasattr(task_format, "Task") or not hasattr(task_format, "Feature"):
        print("FAIL: `Task` or `Feature` TypedDict not found in module.")
        sys.exit(1)

    # Acceptance Criterion 3: The schema covers all required and optional fields.
    Task = task_format.Task
    Feature = task_format.Feature

    required_task_fields = {'id', 'status', 'title', 'action', 'plan', 'features'}
    if not required_task_fields.issubset(Task.__annotations__.keys()):
        missing = required_task_fields - Task.__annotations__.keys()
        print(f"FAIL: Task TypedDict is missing required fields: {missing}")
        sys.exit(1)
        
    required_feature_fields = {'id', 'status', 'title', 'action', 'plan', 'context', 'acceptance'}
    if not required_feature_fields.issubset(Feature.__annotations__.keys()):
        missing = required_feature_fields - Feature.__annotations__.keys()
        print(f"FAIL: Feature TypedDict is missing required fields: {missing}")
        sys.exit(1)

    print("PASS: docs/tasks/task_format.py defines the required Task and Feature TypedDicts.")
    sys.exit(0)

if __name__ == "__main__":
    run()
