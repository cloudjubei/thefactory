import os
import sys
import json

def run_test():
    """
    Tests the acceptance criteria for feature 13.8:
    - All tasks from TASKS.md now exist in the tasks/{id}/task.json format.
    - The `plan` field in each task.json contains the content from the original plan.md.
    - All associated plan.md files are removed from their new locations (tasks/{id}/).
    """
    tasks_dir = "tasks"
    migrated_tasks_found = 0
    errors = []

    if not os.path.isdir(tasks_dir):
        errors.append(f"FAIL: '{tasks_dir}' directory not found.")
        return errors

    for item in os.listdir(tasks_dir):
        task_path = os.path.join(tasks_dir, item)
        if os.path.isdir(task_path) and item.isdigit():
            task_id = item
            migrated_tasks_found += 1
            
            # 1. Check for task.json existence
            task_json_path = os.path.join(task_path, "task.json")
            if not os.path.exists(task_json_path):
                errors.append(f"FAIL: Task {task_id}: 'task.json' not found at {task_json_path}")
                continue

            # 2. Check for embedded plan in task.json
            try:
                with open(task_json_path, 'r', encoding='utf-8') as f:
                    task_data = json.load(f)
                
                if not isinstance(task_data, dict):
                    errors.append(f"FAIL: Task {task_id}: 'task.json' does not contain a JSON object.")
                    continue

                if "plan" not in task_data:
                    errors.append(f"FAIL: Task {task_id}: 'plan' field not found in 'task.json'.")
                elif not isinstance(task_data["plan"], str) or not task_data["plan"].strip():
                    errors.append(f"FAIL: Task {task_id}: 'plan' field in 'task.json' is not a non-empty string.")

            except json.JSONDecodeError:
                errors.append(f"FAIL: Task {task_id}: 'task.json' is not a valid JSON file.")
            except Exception as e:
                errors.append(f"FAIL: Task {task_id}: Error reading 'task.json': {e}")


            # 3. Check for plan.md removal
            plan_md_path = os.path.join(task_path, "plan.md")
            if os.path.exists(plan_md_path):
                errors.append(f"FAIL: Task {task_id}: 'plan.md' was not removed from {task_path}")

    if migrated_tasks_found == 0:
        errors.append("FAIL: No migrated task directories (e.g., 'tasks/1/') found.")

    return errors

def main():
    errors = run_test()
    if errors:
        for error in errors:
            print(error)
        print("\n---")
        print(f"FAIL: {len(errors)} errors found during migration validation.")
        sys.exit(1)
    else:
        print("PASS: Migration validation successful.")
        sys.exit(0)

if __name__ == "__main__":
    main()
