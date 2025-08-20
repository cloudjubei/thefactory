import os
import sys

def run():
    path = "docs/TESTING.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    required_content = [
        "Test Locations and Naming Conventions",
        "tasks/{task_id}/tests/",
        "test_{task_id}_{feature_number}.py",
        "run_tests"
    ]

    missing = [item for item in required_content if item not in content]

    if missing:
        print(f"FAIL: Missing key content in {path}: {', '.join(missing)}")
        sys.exit(1)

    print(f"PASS: {path} exists and describes the testing specification as required.")
    sys.exit(0)

if __name__ == "__main__":
    run()
