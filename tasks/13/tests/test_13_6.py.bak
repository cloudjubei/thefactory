import os
import sys

def run():
    file_path = "scripts/run_local_agent.py"
    print(f"--- Running Test for Feature 13.6: Check orchestrator integration ---")

    # 1. Check if file exists
    if not os.path.exists(file_path):
        print(f"FAIL: {file_path} does not exist.")
        sys.exit(1)
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 2. Check for task_utils import
    if "from scripts.tools.task_utils import get_task" not in content:
        print(f"FAIL: {file_path} does not appear to import the task_utils module.")
        sys.exit(1)
    print("PASS: Orchestrator imports task_utils.")

    # 3. Check for dual-read logic in _gather_context
    if "def _gather_context" not in content:
        print(f"FAIL: Could not find _gather_context function in {file_path}.")
        sys.exit(1)
    
    if "get_task(self.task_id" not in content:
        print(f"FAIL: _gather_context does not appear to call get_task.")
        sys.exit(1)
        
    if "task_json_loaded" not in content or "if filename == 'tasks/TASKS.md' and task_json_loaded:" not in content:
        print(f"FAIL: Could not find dual-read logic to conditionally skip TASKS.md.")
        sys.exit(1)
        
    print("PASS: Orchestrator contains dual-read logic.")
    
    print(f"--- Test for Feature 13.6 PASSED ---")
    sys.exit(0)

if __name__ == "__main__":
    run()
