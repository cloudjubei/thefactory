import os, sys

def run():
    # This test is updated as part of Task 13.4, which moved the original file.
    path = "docs/tasks/TASKS_GUIDANCE.md"
    print(f"--- Running Test for Task 1 (updated for Task 13): Check {path} ---")

    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    required_sections = [
        "# Task Authoring Guidance",
        "## 1. Core Principles",
        "## 2. Field-by-Field Guidance",
        "For the definitive schema and structure, always refer to the Python type definitions in `docs/tasks/task_format.py`"
    ]
    
    missing = [s for s in required_sections if s not in content]
    
    if missing:
        print(f"FAIL: Missing required sections in {path}: " + ", ".join(missing))
        sys.exit(1)
        
    print(f"PASS: {path} exists and contains required sections.")
    sys.exit(0)

if __name__ == "__main__":
    run()
