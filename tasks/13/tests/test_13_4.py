import os
import sys

def run():
    guidance_file = 'docs/tasks/TASKS_GUIDANCE.md'
    if not os.path.exists(guidance_file):
        print(f"FAIL: Guidance file '{guidance_file}' does not exist.")
        sys.exit(1)
    
    with open(guidance_file, 'r') as f:
        content = f.read()
    
    required_refs = [
        '`docs/tasks/task_format.py`',
        '`scripts/tools/task_utils.py`',
        '`docs/tasks/task_example.json`'
    ]
    
    missing = [r for r in required_refs if r not in content]
    
    if missing:
        print(f"FAIL: Guidance file is missing references to: {', '.join(missing)}")
        sys.exit(1)

    print("PASS: TASKS_GUIDANCE.md contains all required references.")
    sys.exit(0)

if __name__ == "__main__":
    run()
