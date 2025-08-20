import os
import sys

def run():
    print("Running test for Feature 1.2: Task Authoring Guidance...")
    
    file_path = "docs/tasks/TASKS_GUIDANCE.md"
    
    # 1. Check for file existence
    if not os.path.exists(file_path):
        print(f"FAIL: {file_path} does not exist.")
        sys.exit(1)
        
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # 2. Check for references
    references = [
        "docs/tasks/task_format.py",
        "docs/tasks/task_example.json",
        "scripts/tools/task_utils.py"
    ]
    
    missing_references = [ref for ref in references if ref not in content]
    
    if missing_references:
        print(f"FAIL: Missing references in {file_path}: {', '.join(missing_references)}")
        sys.exit(1)
        
    print("PASS: docs/tasks/TASKS_GUIDANCE.md exists and contains all required references.")
    sys.exit(0)

if __name__ == "__main__":
    run()
