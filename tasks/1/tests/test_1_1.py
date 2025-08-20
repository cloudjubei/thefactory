import os
import sys

def run():
    print("--- Running Test for Task 1 (updated for Task 13): Check docs/tasks/TASKS_GUIDANCE.md ---")
    guidance_file = 'docs/tasks/TASKS_GUIDANCE.md'
    if not os.path.exists(guidance_file):
        print(f"FAIL: Guidance file '{guidance_file}' does not exist.")
        sys.exit(1)
    
    with open(guidance_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    required_refs = [
        '`docs/tasks/task_format.py`',
        '`scripts/tools/task_utils.py`',
        '`docs/tasks/task_example.json`'
    ]
    
    missing = [r for r in required_refs if r not in content]
    
    if missing:
        print(f"FAIL: {guidance_file} is missing required references: {', '.join(missing)}")
        sys.exit(1)

    print(f"PASS: {guidance_file} contains references to canonical sources.")
    sys.exit(0)

if __name__ == "__main__":
    run()
