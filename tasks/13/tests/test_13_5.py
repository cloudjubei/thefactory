import sys
import os

def run_test():
    file_path = "scripts/run_local_agent.py"
    if not os.path.exists(file_path):
        print(f"FAIL: {file_path} does not exist.")
        sys.exit(1)

    with open(file_path, "r") as f:
        content = f.read()

    import_string = "from scripts.tools.task_utils import get_task"
    if import_string not in content:
        print(f"FAIL: Required import '{import_string}' not found in {file_path}.")
        sys.exit(1)

    usage_string = "get_task(self.task_id,"
    if usage_string not in content:
        print(f"FAIL: Required usage of 'get_task' not found in {file_path}.")
        sys.exit(1)

    print("PASS: `run_local_agent.py` correctly imports and uses `task_utils.py`.")
    sys.exit(0)

if __name__ == "__main__":
    run_test()
