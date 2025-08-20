import os
import sys

def run():
    print("Running test for Feature 13.10: Remove TASKS.md")
    errors = []

    tasks_md_path = 'tasks/TASKS.md'
    if os.path.exists(tasks_md_path):
        errors.append(f"FAIL: {tasks_md_path} still exists.")

    if errors:
        for error in errors:
            print(error)
        sys.exit(1)

    print("PASS: Feature 13.10 test checks passed.")
    sys.exit(0)

if __name__ == "__main__":
    run()
