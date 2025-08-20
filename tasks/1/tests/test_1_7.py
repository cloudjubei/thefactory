import os
import sys

def run():
    path = "docs/PLAN_SPECIFICATION.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    references = [
        "docs/tasks/task_format.py",
        "docs/tasks/task_example.json",
        "docs/tasks/TASKS_GUIDANCE.md",
        "docs/TESTING.md"
    ]
    
    explanations = [
        "step-by-step plan",
        "acceptance criteria",
        "finish_feature",
        "submit_for_review"
    ]
    
    required = references + explanations
    missing = [item for item in required if item not in content]

    if missing:
        print(f"FAIL: Missing required content/references in {path}: {', '.join(missing)}")
        sys.exit(1)

    print(f"PASS: {path} exists and contains all required references and explanations.")
    sys.exit(0)

if __name__ == "__main__":
    run()
