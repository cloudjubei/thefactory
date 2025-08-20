import os
import sys
import json

def run():
    print("Running test for Feature 13.12: Cleanup")
    errors = []

    # AC: all tasks folders only have the tests folder and a `task.json` file
    tasks_dir = 'tasks'
    if os.path.isdir(tasks_dir):
        for entry in os.listdir(tasks_dir):
            task_path = os.path.join(tasks_dir, entry)
            if os.path.isdir(task_path) and entry.isdigit():
                allowed_contents = {'task.json', 'tests'}
                actual_contents = set(os.listdir(task_path))
                disallowed_contents = actual_contents - allowed_contents
                if disallowed_contents:
                    errors.append(f"FAIL: Task directory {task_path} contains unexpected files/dirs: {disallowed_contents}")

    # AC: Task 1 needs to be updated to reflect the new JSON-based format
    task_1_path = 'tasks/1/task.json'
    if os.path.exists(task_1_path):
        with open(task_1_path, 'r', encoding='utf-8') as f:
            try:
                task_1_data = json.load(f)
                title_and_action = task_1_data.get('title', '') + task_1_data.get('action', '')
                if 'json' not in title_and_action.lower():
                    errors.append(f"FAIL: Task 1 ({task_1_path}) does not seem to be updated to reflect the new JSON-based format.")
            except json.JSONDecodeError:
                errors.append(f"FAIL: Could not parse JSON from {task_1_path}")

    if errors:
        for error in errors:
            print(error)
        sys.exit(1)

    print("PASS: Feature 13.12 test checks passed.")
    sys.exit(0)

if __name__ == "__main__":
    run()
