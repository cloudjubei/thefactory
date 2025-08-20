import sys
import os

def run():
    file_path = "docs/tasks/TASKS_GUIDANCE.md"
    if not os.path.exists(file_path):
        print(f"FAIL: {file_path} does not exist.")
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    references = [
        "docs/tasks/task_format.py",
        "docs/tasks/task_example.json",
        "scripts/tools/task_utils.py"
    ]

    missing = [ref for ref in references if ref not in content]

    if missing:
        print(f"FAIL: Missing references in {file_path}: {', '.join(missing)}")
        sys.exit(1)

    print("PASS: docs/tasks/TASKS_GUIDANCE.md exists and contains all required references.")
    sys.exit(0)

if __name__ == "__main__":
    run()
