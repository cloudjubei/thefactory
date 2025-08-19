import os
import sys
import json

def run():
    file_path = "docs/tasks/task_example.json"
    print(f"--- Running Test for Feature 13.2: Check {file_path} ---")

    if not os.path.exists(file_path):
        print(f"FAIL: {file_path} does not exist.")
        sys.exit(1)

    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"FAIL: {file_path} is not a valid JSON file: {e}")
        sys.exit(1)

    required_keys = ['id', 'title', 'action', 'status', 'acceptance_criteria', 'features']
    missing_keys = [k for k in required_keys if k not in data]
    if missing_keys:
        print(f"FAIL: {file_path} is missing required top-level keys: {', '.join(missing_keys)}")
        sys.exit(1)

    print(f"PASS: {file_path} exists, is valid JSON, and contains required keys.")
    sys.exit(0)

if __name__ == "__main__":
    run()
