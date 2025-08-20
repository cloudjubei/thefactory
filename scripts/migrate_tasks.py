import os
import json
import re

def parse_plan_md(content):
    """
    Parses the content of a plan.md file into a main plan and a dict of feature plans.
    """
    # Split by feature headings
    feature_pattern = re.compile(r'###\s+([\d\.]+)\s+.*')
    sections = feature_pattern.split(content)
    
    # The first section is the main task plan
    main_plan = sections[0].strip()
    
    feature_plans = {}
    if len(sections) > 1:
        for i in range(1, len(sections), 2):
            feature_id = sections[i]
            feature_plan_content = sections[i+1].strip()
            feature_plans[feature_id] = feature_plan_content
            
    return main_plan, feature_plans

def migrate_task(task_path):
    """
    Migrates a single task by embedding its plan.md into task.json.
    """
    task_json_path = os.path.join(task_path, 'task.json')
    plan_md_path = os.path.join(task_path, 'plan.md')

    if not os.path.exists(plan_md_path):
        print(f"INFO: No plan.md found for task at {task_path}, skipping.")
        return False

    if not os.path.exists(task_json_path):
        print(f"ERROR: task.json not found for task at {task_path}, cannot migrate plan.")
        return False

    print(f"Migrating plan for task: {task_path}")

    try:
        with open(task_json_path, 'r') as f:
            task_data = json.load(f)

        with open(plan_md_path, 'r') as f:
            plan_content = f.read()

        main_plan, feature_plans = parse_plan_md(plan_content)

        task_data['plan'] = (task_data.get('plan', '') + '\n' + main_plan).strip()

        if 'features' in task_data:
            for feature in task_data['features']:
                f_id = feature.get('id')
                if f_id in feature_plans:
                    feature['plan'] = (feature.get('plan', '') + '\n' + feature_plans[f_id]).strip()

        with open(task_json_path, 'w') as f:
            json.dump(task_data, f, indent=2)

        os.remove(plan_md_path)
        print(f"Successfully migrated and removed {plan_md_path}")
        return True

    except Exception as e:
        print(f"ERROR: Failed to migrate task at {task_path}: {e}")
        return False

def main():
    """
    Main function to run the migration for all tasks.
    """
    tasks_dir = 'tasks'
    if not os.path.isdir(tasks_dir):
        print(f"ERROR: Directory '{tasks_dir}' not found.")
        return

    migrated_count = 0
    for task_id_str in os.listdir(tasks_dir):
        task_path = os.path.join(tasks_dir, task_id_str)
        if os.path.isdir(task_path) and task_id_str.isdigit():
            if migrate_task(task_path):
                migrated_count += 1
    
    print(f"\nMigration complete. Migrated {migrated_count} task(s).")

if __name__ == '__main__':
    main()
