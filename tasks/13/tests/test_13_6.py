import os
import sys

def run():
    file_path = "scripts/run_local_agent.py"
    print(f"--- Running Test for Feature 13.6: Check orchestrator integration ---")

    if not os.path.exists(file_path):
        print(f"FAIL: {file_path} does not exist (this should not happen).")
        sys.exit(1)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        import_string_1 = "from scripts.tools.task_utils"
        import_string_2 = "import task_utils"
        
        if import_string_1 not in content and import_string_2 not in content:
            print(f"FAIL: {file_path} does not appear to import the task_utils module.")
            sys.exit(1)

    except Exception as e:
        print(f"FAIL: An error occurred while reading {file_path}: {e}")
        sys.exit(1)

    print(f"PASS: {file_path} seems to be updated to import task_utils.")
    sys.exit(0)

if __name__ == "__main__":
    run()
