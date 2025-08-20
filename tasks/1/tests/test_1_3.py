import os
import sys
import json

def run():
    path = "docs/tasks/task_example.json"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"FAIL: {path} is not a valid JSON file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"FAIL: Could not read {path}: {e}")
        sys.exit(1)

    required_task_keys = ["id", "status", "title", "action", "plan", "features"]
    if not all(key in data for key in required_task_keys):
        print(f"FAIL: Missing required top-level keys in {path}. Required: {required_task_keys}")
        sys.exit(1)
    
    if not isinstance(data.get("features"), list) or not data["features"]:
        print(f"FAIL: 'features' key in {path} is not a non-empty list.")
        sys.exit(1)

    first_feature = data["features"][0]
    required_feature_keys = ["id", "status", "title", "action", "plan", "acceptance"]
    if not all(key in first_feature for key in required_feature_keys):
        print(f"FAIL: Missing required feature keys in {path}. Required: {required_feature_keys}")
        sys.exit(1)

    print(f"PASS: {path} exists, is valid JSON, and conforms to the basic Task schema.")
    sys.exit(0)

if __name__ == "__main__":
    run()
