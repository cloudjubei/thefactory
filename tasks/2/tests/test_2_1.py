import os
import sys
import json
import shutil
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from scripts.tools.task_utils import move_task_logic, get_all_tasks

def setup_test_tasks(base_dir):
    task1_data = {
        "id": 1, "title": "Task 1", "features": [
            {"id": "1.1", "dependencies": []}
        ]
    }
    task2_data = {
        "id": 2, "title": "Task 2", "features": [
            {"id": "2.1", "dependencies": ["1.1"]}
        ]
    }
    task3_data = {
        "id": 3, "title": "Task 3", "features": [
            {"id": "3.1", "dependencies": []}
        ]
    }

    for task_data in [task1_data, task2_data, task3_data]:
        task_dir = os.path.join(base_dir, str(task_data['id']))
        os.makedirs(task_dir)
        with open(os.path.join(task_dir, 'task.json'), 'w') as f:
            json.dump(task_data, f)

def run():
    orchestrator_path = 'scripts/run_local_agent.py'
    if not os.path.exists(orchestrator_path):
        print(f"FAIL: {orchestrator_path} does not exist.")
        sys.exit(1)
    
    with open(orchestrator_path, 'r') as f:
        content = f.read()
    
    required_tools = [
        'write_file', 'retrieve_context_files', 'rename_files',
        'submit_for_review', 'ask_question', 'finish',
        'finish_feature', 'move_task'
    ]
    
    missing_tools = []
    for tool in required_tools:
        if f'def {tool}(' not in content:
            missing_tools.append(tool)
    
    if missing_tools:
        print(f"FAIL: Orchestrator is missing tool definitions: {', '.join(missing_tools)}")
        sys.exit(1)

    temp_dir = tempfile.mkdtemp()
    try:
        tasks_base = os.path.join(temp_dir, 'tasks')
        os.makedirs(tasks_base)
        setup_test_tasks(tasks_base)

        result = move_task_logic(3, 1, tasks_base)
        if not result.get('ok'):
            print(f"FAIL: move_task_logic failed: {result.get('error')}")
            sys.exit(1)
        
        new_tasks = get_all_tasks(tasks_base)
        if len(new_tasks) != 3:
            print(f"FAIL: Expected 3 tasks, found {len(new_tasks)}")
            sys.exit(1)

        if new_tasks[0]['title'] != 'Task 3' or new_tasks[0]['id'] != 1:
            print(f"FAIL: Task at index 0 is incorrect. Got ID {new_tasks[0]['id']} Title {new_tasks[0]['title']}")
            sys.exit(1)

        if new_tasks[1]['title'] != 'Task 1' or new_tasks[1]['id'] != 2:
            print(f"FAIL: Task at index 1 is incorrect. Got ID {new_tasks[1]['id']} Title {new_tasks[1]['title']}")
            sys.exit(1)

        if new_tasks[2]['title'] != 'Task 2' or new_tasks[2]['id'] != 3:
            print(f"FAIL: Task at index 2 is incorrect. Got ID {new_tasks[2]['id']} Title {new_tasks[2]['title']}")
            sys.exit(1)

        dep = new_tasks[2]['features'][0]['dependencies'][0]
        if dep != '2.1':
            print(f"FAIL: Dependency not updated correctly. Expected '2.1', got '{dep}'")
            sys.exit(1)

    finally:
        shutil.rmtree(temp_dir)

    print("PASS: Orchestrator script and move_task logic are valid.")
    sys.exit(0)

if __name__ == "__main__":
    run()
