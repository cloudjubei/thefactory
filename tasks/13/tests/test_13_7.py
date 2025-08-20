import json
import sys
import os

def run():
    # Check that Task 1 has been updated correctly
    task_1_file = 'tasks/1/task.json'
    if not os.path.exists(task_1_file):
        print(f"FAIL: {task_1_file} does not exist.")
        sys.exit(1)

    with open(task_1_file, 'r') as f:
        task_1_data = json.load(f)

    if task_1_data.get('title') != 'Task Management System Definition':
        print(f"FAIL: Task 1 title is incorrect.")
        sys.exit(1)

    feature_ids = [f['id'] for f in task_1_data.get('features', [])]
    expected_features = ['1.1', '1.2', '1.3', '1.4']
    if sorted(feature_ids) != expected_features:
        print(f"FAIL: Task 1 does not contain the expected features. Found {feature_ids}")
        sys.exit(1)

    # Check that Task 13's feature 13.7 is marked as complete
    task_13_file = 'tasks/13/task.json'
    if not os.path.exists(task_13_file):
        print(f"FAIL: {task_13_file} does not exist.")
        sys.exit(1)

    with open(task_13_file, 'r') as f:
        task_13_data = json.load(f)
    
    feature_13_7 = next((f for f in task_13_data.get('features', []) if f['id'] == '13.7'), None)
    if not feature_13_7:
        print("FAIL: Feature 13.7 not found in Task 13.")
        sys.exit(1)

    if feature_13_7.get('status') != '+':
        print("FAIL: Feature 13.7 is not marked as complete ('+').")
        sys.exit(1)

    print("PASS: Task 1 successfully updated and feature 13.7 marked as complete.")
    sys.exit(0)

if __name__ == "__main__":
    run()
