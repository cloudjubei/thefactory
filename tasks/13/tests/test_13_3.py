import os
import sys
import inspect

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

try:
    from scripts.tools import task_utils
except ImportError as e:
    print(f"FAIL: Could not import scripts.tools.task_utils: {e}")
    sys.exit(1)

def run():
    required_functions = [
        'get_task',
        'update_task',
        'create_task',
        'update_task_status',
        'update_feature_status',
        'ask_agent_question'
    ]
    
    actual_functions = [name for name, func in inspect.getmembers(task_utils, inspect.isfunction)]
    
    missing = [f for f in required_functions if f not in actual_functions]
    
    if missing:
        print(f"FAIL: task_utils.py is missing functions: {', '.join(missing)}")
        sys.exit(1)
        
    print("PASS: task_utils.py exists and has all required functions.")
    sys.exit(0)

if __name__ == "__main__":
    run()
