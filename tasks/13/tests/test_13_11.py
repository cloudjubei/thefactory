import os
import sys
import json
import shutil

# Add scripts/tools to the path to allow direct import of task_utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../scripts/tools')))

import task_utils

def setup_test_task():
    "Create a dummy task directory and task.json for testing." 
    test_task_dir = "tasks/999"
    os.makedirs(test_task_dir, exist_ok=True)
    dummy_task_data = {
        "id": 999,
        "status": "-",
        "title": "Dummy Task",
        "features": [
            {
                "id": "999.1",
                "status": "-",
                "title": "Dummy Feature"
            }
        ]
    }
    with open(os.path.join(test_task_dir, "task.json"), "w") as f:
        json.dump(dummy_task_data, f, indent=2)
    return 999, "999.1"

def cleanup_test_task():
    "Remove the dummy task directory."
    test_task_dir = "tasks/999"
    if os.path.exists(test_task_dir):
        shutil.rmtree(test_task_dir)

def run():
    try:
        # 1. Test the new function in task_utils.py
        print("--- Testing task_utils.update_feature_status ---")
        task_id, feature_id = setup_test_task()
        
        # Test successful update
        success = task_utils.update_feature_status(task_id, feature_id, "+")
        if not success:
            print("FAIL: update_feature_status returned False on success case.")
            sys.exit(1)
        
        updated_task = task_utils.get_task(task_id)
        if not updated_task or updated_task['features'][0]['status'] != "+":
            print("FAIL: Feature status was not updated correctly in task.json.")
            sys.exit(1)
        print("PASS: task_utils.update_feature_status works as expected.")

        # 2. Check PLAN_SPECIFICATION.md for updates
        print("--- Checking docs/PLAN_SPECIFICATION.md ---")
        with open("docs/PLAN_SPECIFICATION.md", "r") as f:
            content = f.read()
        if "plan.md" in content or "plan_" in content:
            print("FAIL: docs/PLAN_SPECIFICATION.md still contains references to plan.md")
            sys.exit(1)
        if "task.json" not in content:
            print("FAIL: docs/PLAN_SPECIFICATION.md does not reference task.json")
            sys.exit(1)
        print("PASS: docs/PLAN_SPECIFICATION.md is updated.")

        # 3. Check FILE_ORGANISATION.md for updates
        print("--- Checking docs/FILE_ORGANISATION.md ---")
        with open("docs/FILE_ORGANISATION.md", "r") as f:
            content = f.read()
        if "plan.md" in content or "plan_" in content:
            print("FAIL: docs/FILE_ORGANISATION.md still contains references to plan.md")
            sys.exit(1)
        print("PASS: docs/FILE_ORGANISATION.md is updated.")

    finally:
        cleanup_test_task()

    # If all checks passed
    sys.exit(0)

if __name__ == "__main__":
    run()
