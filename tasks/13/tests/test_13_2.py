import os
import sys
import json

def run():
    file_path = "docs/tasks/task_example.json"
    print(f"--- Running Test for Feature 13.2: {file_path} ---")

    # 1. Check if file exists
    if not os.path.exists(file_path):
        print(f"FAIL: File '{file_path}' does not exist.")
        sys.exit(1)
    
    print(f"PASS: File '{file_path}' exists.")

    # 2. Check if content is valid JSON
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"FAIL: File '{file_path}' contains invalid JSON: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"FAIL: Could not read file '{file_path}': {e}")
        sys.exit(1)

    print("PASS: File content is valid JSON.")

    # 3. Check for essential top-level keys
    required_keys = ["id", "title", "status", "action", "acceptance", "features"]
    missing_keys = [key for key in required_keys if key not in data]

    if missing_keys:
        print(f"FAIL: Missing required top-level keys in JSON: {', '.join(missing_keys)}")
        sys.exit(1)

    print(f"PASS: All required top-level keys found: {', '.join(required_keys)}.")

    # If all checks pass
    print(f"--- Test for Feature 13.2 PASSED ---")
    sys.exit(0)

if __name__ == "__main__":
    run()
