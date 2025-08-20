import os
import sys

def run():
    path = "docs/tasks/TASKS_GUIDANCE.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    references = [
        "docs/tasks/task_format.py",
        "docs/tasks/task_example.json",
        "scripts/tools/task_utils.py"
    ]
    
    missing = [ref for ref in references if ref not in content]
    
    if missing:
        print(f"FAIL: Missing references in {path}: {', '.join(missing)}")
        sys.exit(1)
        
    print(f"PASS: {path} exists and contains all required references.")
    sys.exit(0)

if __name__ == "__main__":
    run()
