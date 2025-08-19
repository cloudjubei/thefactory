import os
import sys

def run():
    file_path = "docs/tasks/TASKS_MIGRATION_GUIDE.md"
    print(f"--- Running Test for Feature 13.3: Check {file_path} ---")

    if not os.path.exists(file_path):
        print(f"FAIL: {file_path} does not exist.")
        sys.exit(1)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"FAIL: An error occurred while reading {file_path}: {e}")
        sys.exit(1)

    required_headings = [
        "Migration Plan",
        "Backward Compatibility",
        "Tooling Requirements",
        "Rollback Plan"
    ]
    missing_headings = [h for h in required_headings if h not in content]
    if missing_headings:
        print(f"FAIL: {file_path} is missing required sections: {', '.join(missing_headings)}")
        sys.exit(1)

    print(f"PASS: {file_path} exists and contains all required sections.")
    sys.exit(0)

if __name__ == "__main__":
    run()
