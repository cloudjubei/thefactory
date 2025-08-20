import os
import sys
import json

def run():
    """
    Verifies that the task.json file for task 13 has a 'plan' field
    at the top level and for every feature.
    """
    task_file_path = "tasks/13/task.json"
    if not os.path.exists(task_file_path):
        print(f"FAIL: {task_file_path} does not exist.")
        sys.exit(1)

    try:
        with open(task_file_path, "r", encoding="utf-8") as f:
            task_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"FAIL: Could not decode JSON from {task_file_path}: {e}")
        sys.exit(1)

    # Check top-level plan
    if "plan" not in task_data or not isinstance(task_data["plan"], str) or not task_data["plan"].strip():
        print(f"FAIL: Top-level 'plan' field is missing, not a string, or empty in {task_file_path}.")
        sys.exit(1)

    # Check feature-level plans
    if "features" not in task_data or not isinstance(task_data["features"], list):
        print(f"FAIL: 'features' field is missing or not a list in {task_file_path}.")
        sys.exit(1)
        
    all_features_have_plan = True
    for i, feature in enumerate(task_data["features"]):
        if "plan" not in feature or not isinstance(feature["plan"], str) or not feature["plan"].strip():
            print(f"FAIL: Feature #{i+1} (ID: {feature.get('id', 'N/A')}) is missing a 'plan', or it is not a non-empty string.")
            all_features_have_plan = False

    if not all_features_have_plan:
        sys.exit(1)

    print("PASS: Top-level plan and all feature plans exist and are non-empty strings.")
    sys.exit(0)

if __name__ == "__main__":
    run()
