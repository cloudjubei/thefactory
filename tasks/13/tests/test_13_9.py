import os
import sys

def run():
    file_path = "scripts/run_local_agent.py"
    print(f"--- Running Test for Feature 13.9: Check removal of dual-read mode ---")

    if not os.path.exists(file_path):
        print(f"FAIL: {file_path} does not exist.")
        sys.exit(1)
        
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if "tasks/TASKS.md" in content:
            print(f"FAIL: {file_path} still contains references to 'tasks/TASKS.md'. Dual-read mode may not be removed.")
            sys.exit(1)
            
    except Exception as e:
        print(f"FAIL: An error occurred while reading {file_path}: {e}")
        sys.exit(1)
        
    print(f"PASS: Orchestrator appears to have dual-read mode removed.")
    sys.exit(0)

if __name__ == "__main__":
    run()
