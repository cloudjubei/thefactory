import os
import sys

def run():
    file_path = "scripts/tools/task_utils.py"
    print(f"--- Running Test for Feature 13.5: Check {file_path} ---")

    # 1. Check if file exists
    if not os.path.exists(file_path):
        print(f"FAIL: {file_path} does not exist.")
        sys.exit(1)
    
    print(f"PASS: File '{file_path}' exists.")

    # 2. Check for required function definitions
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    required_functions = [
        "def get_task",
        "def update_task",
        "def create_task"
    ]
    
    missing_functions = [func for func in required_functions if func not in content]

    if missing_functions:
        print(f"FAIL: Missing required function definitions in {file_path}: {', '.join(missing_functions)}")
        sys.exit(1)

    print(f"PASS: All required functions are present in '{file_path}'.")
    
    print(f"--- Test for Feature 13.5 PASSED ---")
    sys.exit(0)

if __name__ == "__main__":
    run()
