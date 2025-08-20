import os
import sys
import json
import tempfile
import shutil

# Add scripts/tools to path to allow importing task_utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../scripts/tools')))
try:
    import task_utils
except ImportError:
    print("FAIL: Could not import task_utils. Make sure it is in scripts/tools.")
    sys.exit(1)

def run():
    # Create a temporary directory to simulate a tasks folder
    temp_dir = tempfile.mkdtemp()
    task_id_str = "999"
    task_id_int = 999
    task_dir = os.path.join(temp_dir, task_id_str)
    os.makedirs(task_dir)

    try:
        # 1. Test case: task.json exists, plan.md does not. Should succeed.
        print("Test 1: Reading task from task.json only...")
        task_data = {"id": 999, "title": "Test Task", "plan": ""}
        task_json_path = os.path.join(task_dir, 'task.json')
        with open(task_json_path, 'w') as f:
            json.dump(task_data, f)

        retrieved_task = task_utils.get_task(task_id_int, base_path=temp_dir)
        if not retrieved_task or retrieved_task['id'] != 999:
            print(f"FAIL: get_task failed to read task.json. Got: {retrieved_task}")
            sys.exit(1)
        print("PASS: get_task successfully read from task.json.")

        # 2. Test case: task.json exists, and a rogue plan.md exists.
        #    The function should IGNORE plan.md.
        print("\nTest 2: Ignoring plan.md when reading task...")
        plan_md_path = os.path.join(task_dir, 'plan.md')
        with open(plan_md_path, 'w') as f:
            f.write("This is a plan that should be ignored.")
        
        task_data_with_plan = {"id": 999, "title": "Test Task", "plan": "Original plan in json"}
        with open(task_json_path, 'w') as f:
            json.dump(task_data_with_plan, f)
        
        retrieved_task_2 = task_utils.get_task(task_id_int, base_path=temp_dir)
        if not retrieved_task_2 or retrieved_task_2.get('plan') != "Original plan in json":
            print(f"FAIL: get_task was modified by plan.md. Plan content: '{retrieved_task_2.get('plan')}'")
            sys.exit(1)
        print("PASS: get_task correctly ignored plan.md.")

        # 3. Test case: task file does not exist
        print("\nTest 3: Handling non-existent task...")
        retrieved_task_3 = task_utils.get_task(1000, base_path=temp_dir)
        if retrieved_task_3 is not None:
            print(f"FAIL: get_task should return None for non-existent task, but got {retrieved_task_3}")
            sys.exit(1)
        print("PASS: get_task correctly returned None for a non-existent task.")

    finally:
        # Clean up the temporary directory
        shutil.rmtree(temp_dir)

    print("\nAll tests for feature 13.8 passed!")
    sys.exit(0)

if __name__ == "__main__":
    run()
