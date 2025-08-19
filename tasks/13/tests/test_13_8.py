import os
import sys
import json

def run():
    print("Running test for migration (feature 13.8)...")
    errors = []

    # Check for new task.json files
    task_files_to_check = ["tasks/6/task.json", "tasks/13/task.json", "tasks/24/task.json"]
    for path in task_files_to_check:
        if not os.path.exists(path):
            errors.append(f"FAIL: Migrated task file {path} does not exist.")

    # Check content of a task.json file
    task_13_path = "tasks/13/task.json"
    if os.path.exists(task_13_path):
        try:
            with open(task_13_path, "r") as f:
                data = json.load(f)
            if data.get("id") != 13:
                errors.append(f"FAIL: {task_13_path} has incorrect id.")
            if "JSON-based tasks format" not in data.get("title", ""):
                errors.append(f"FAIL: {task_13_path} has incorrect title.")
            if not isinstance(data.get("features"), list) or len(data.get("features", [])) == 0:
                errors.append(f"FAIL: {task_13_path} should contain features.")
        except Exception as e:
            errors.append(f"FAIL: Could not read or parse {task_13_path}: {e}")
    else:
        errors.append(f"FAIL: {task_13_path} does not exist for content check.")


    # Check for renamed plan file
    if not os.path.exists("tasks/13/plan.md"):
        errors.append("FAIL: Plan file tasks/13/plan.md was not created/renamed.")
    if os.path.exists("tasks/13/plan_13.md"):
        errors.append("FAIL: Old plan file tasks/13/plan_13.md was not removed.")

    if errors:
        for error in errors:
            print(error)
        sys.exit(1)
    
    print("PASS: Task migration verified successfully.")
    sys.exit(0)

if __name__ == "__main__":
    run()
