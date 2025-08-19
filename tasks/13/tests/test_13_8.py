import os
import sys

def run():
    print(f"--- Running Test for Feature 13.8: Validate migration results ---")

    tasks_dir = "tasks"
    expected_task_file = os.path.join(tasks_dir, "13", "task.json")
    expected_plan_file = os.path.join(tasks_dir, "13", "plan_13.md")

    if not os.path.exists(expected_task_file):
        print(f"FAIL: Migrated task file {expected_task_file} does not exist.")
        sys.exit(1)
        
    if not os.path.exists(expected_plan_file):
        print(f"FAIL: Migrated plan file {expected_plan_file} does not exist.")
        sys.exit(1)
        
    print("PASS: Key migrated files exist in the new structure.")
    sys.exit(0)

if __name__ == "__main__":
    run()
