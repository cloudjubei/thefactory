import os
import sys
import importlib.util

def run():
    file_path = "docs/tasks/task_format.py"
    print(f"--- Running Test for Feature 13.1: Check {file_path} ---")

    if not os.path.exists(file_path):
        print(f"FAIL: {file_path} does not exist.")
        sys.exit(1)

    try:
        spec = importlib.util.spec_from_file_location("task_format", file_path)
        task_format = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(task_format)

        required_types = ["Task", "Feature"]
        missing_types = [t for t in required_types if not hasattr(task_format, t)]

        if missing_types:
            print(f"FAIL: {file_path} is missing required type definitions: {', '.join(missing_types)}")
            sys.exit(1)

        task_type = getattr(task_format, "Task")
        if hasattr(task_type, '__annotations__'):
            task_annotations = task_type.__annotations__
            required_fields = ['id', 'title', 'action', 'status']
            missing_fields = [f for f in required_fields if f not in task_annotations]
            if missing_fields:
                print(f"FAIL: The 'Task' type is missing required fields: {', '.join(missing_fields)}")
                sys.exit(1)
        else:
            print("WARNING: Could not check annotations for Task type.")

    except Exception as e:
        print(f"FAIL: An error occurred while inspecting {file_path}: {e}")
        sys.exit(1)

    print(f"PASS: {file_path} exists and defines the required types.")
    sys.exit(0)

if __name__ == "__main__":
    run()
