import os
import sys
import importlib.util

def run():
    print("Running test for Feature 1.4: Task Utility Tooling...")
    
    file_path = "scripts/tools/task_utils.py"
    
    # 1. Check for file existence
    if not os.path.exists(file_path):
        print(f"FAIL: {file_path} does not exist.")
        sys.exit(1)
        
    # 2. Check for required functions
    try:
        spec = importlib.util.spec_from_file_location("task_utils", file_path)
        task_utils = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(task_utils)
    except Exception as e:
        print(f"FAIL: Could not import module from {file_path}. Error: {e}")
        sys.exit(1)
        
    required_functions = [
        "get_task",
        "update_task",
        "create_task"
    ]
    
    missing_functions = [func for func in required_functions if not hasattr(task_utils, func)]
    
    if missing_functions:
        print(f"FAIL: Missing functions in {file_path}: {', '.join(missing_functions)}")
        sys.exit(1)
        
    # 3. Check if task_format is imported as a proxy for schema conformance
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    if "from docs.tasks.task_format import" not in content and "import docs.tasks.task_format" not in content:
        print(f"WARNING: {file_path} does not seem to import the canonical schema from docs/tasks/task_format.py. Manual check advised.")

    print("PASS: scripts/tools/task_utils.py exists and provides the required functions.")
    sys.exit(0)

if __name__ == "__main__":
    run()
