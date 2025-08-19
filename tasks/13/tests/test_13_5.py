import os
import sys
import importlib.util

def run():
    file_path = "scripts/tools/task_utils.py"
    print(f"--- Running Test for Feature 13.5: Check {file_path} ---")

    if not os.path.exists(file_path):
        print(f"FAIL: {file_path} does not exist.")
        sys.exit(1)

    try:
        spec = importlib.util.spec_from_file_location("task_utils", file_path)
        task_utils = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(task_utils)

        required_functions = ["get_task", "update_task", "create_task"]
        missing_functions = [f for f in required_functions if not hasattr(task_utils, f) or not callable(getattr(task_utils, f))]

        if missing_functions:
            print(f"FAIL: {file_path} is missing required functions: {', '.join(missing_functions)}")
            sys.exit(1)

    except Exception as e:
        print(f"FAIL: An error occurred while inspecting {file_path}: {e}")
        sys.exit(1)

    print(f"PASS: {file_path} exists and defines the required utility functions.")
    sys.exit(0)

if __name__ == "__main__":
    run()
