import os
import sys

def run():
    old_path = "docs/TASK_FORMAT.md"
    new_path = "docs/tasks/TASKS_GUIDANCE.md"
    print(f"--- Running Test for Feature 13.4: Check file move and update ---")

    if os.path.exists(old_path):
        print(f"FAIL: The old file {old_path} still exists.")
        sys.exit(1)

    if not os.path.exists(new_path):
        print(f"FAIL: The new file {new_path} does not exist.")
        sys.exit(1)

    try:
        with open(new_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if "JSON" not in content and "json" not in content:
             print(f"FAIL: {new_path} does not seem to be updated to mention the JSON format.")
             sys.exit(1)
    except Exception as e:
        print(f"FAIL: An error occurred while reading {new_path}: {e}")
        sys.exit(1)

    print("PASS: Task format documentation has been moved and updated successfully.")
    sys.exit(0)

if __name__ == "__main__":
    run()
