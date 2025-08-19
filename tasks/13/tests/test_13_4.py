import os
import sys

def run():
    old_path = "docs/TASK_FORMAT.md"
    new_path = "docs/tasks/TASKS_GUIDANCE.md"
    print(f"--- Running Test for Feature 13.4: Check file move and update ---")

    # 1. Check that the old file is removed
    if os.path.exists(old_path):
        print(f"FAIL: The old file {old_path} still exists.")
        sys.exit(1)
    print(f"PASS: Old file '{old_path}' is removed.")

    # 2. Check that the new file exists
    if not os.path.exists(new_path):
        print(f"FAIL: The new file {new_path} does not exist.")
        sys.exit(1)
    print(f"PASS: New file '{new_path}' exists.")

    # 3. Check that the content is updated
    with open(new_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    if "task_format.py" not in content:
        print(f"FAIL: Content of {new_path} does not seem to be updated for the JSON format (missing reference to 'task_format.py').")
        sys.exit(1)
    
    if "TASKS.md" in content:
        print(f"FAIL: Content of {new_path} still contains references to the old 'TASKS.md' format.")
        sys.exit(1)

    print(f"PASS: Content of '{new_path}' is updated.")

    print(f"--- Test for Feature 13.4 PASSED ---")
    sys.exit(0)

if __name__ == "__main__":
    run()
