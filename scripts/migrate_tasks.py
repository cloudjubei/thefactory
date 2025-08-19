import os
import re
import json
import sys

# Add scripts directory to path to allow import of task_utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tools.task_utils import get_task

TASKS_FILE = "tasks/TASKS.md"
TASKS_DIR = "tasks"

def parse_plan_md(content):
    """
    Parses the content of a plan.md file to extract the overall plan
    and the plan for each feature.
    """
    plan_data = {"overall": "", "features": {}}
    
    intent_match = re.search(r"## Intent\s*\n(.*?)(?=\n##|$)", content, re.DOTALL)
    if intent_match:
        plan_data["overall"] = intent_match.group(1).strip()

    features_section_match = re.search(r"## Features\s*\n(.*?)(?=\n##|$)", content, re.DOTALL)
    if not features_section_match:
        return plan_data

    features_content = features_section_match.group(1)
    
    # Split by feature headers like "13.1) + ..." at the beginning of a line
    feature_blocks = re.split(r'\n(?=^\d+\.\d+\))', features_content.strip())
    
    for block in feature_blocks:
        if not block.strip():
            continue
        
        id_match = re.match(r'^\s*(\d+\.\d+)\)', block.strip())
        if id_match:
            feature_id = id_match.group(1)
            # The plan for the feature is its entire definition block from the plan.md
            plan_data["features"][feature_id] = block.strip()
            
    return plan_data


def embed_plan_and_cleanup(task_id_str):
    """
    Reads plan.md for a task, embeds its content into task.json,
    and then deletes plan.md.
    """
    task_id = int(task_id_str)
    task_dir = os.path.join(TASKS_DIR, task_id_str)
    plan_path = os.path.join(task_dir, "plan.md")
    task_json_path = os.path.join(task_dir, "task.json")
    
    if not os.path.exists(plan_path):
        # This is not an error; it might have been run before or the task has no plan.md
        return

    print(f"Embedding plan for task {task_id}...")
    with open(plan_path, 'r', encoding='utf-8') as f:
        plan_content = f.read()
    
    plan_data = parse_plan_md(plan_content)
    
    # Use get_task which we know exists and works
    task_data = get_task(task_id, base_path=TASKS_DIR)
    if not task_data:
        print(f"Warning: Could not read task.json for task {task_id}. Skipping.")
        return

    # Embed the overall plan
    task_data["plan"] = plan_data.get("overall", "")
    
    # Embed feature-specific plans
    if "features" in task_data:
        for feature in task_data["features"]:
            feature_id = feature.get("id")
            if feature_id and feature_id in plan_data["features"]:
                feature["plan"] = plan_data["features"][feature_id]

    # Write the updated task data back to task.json
    try:
        with open(task_json_path, 'w', encoding='utf-8') as f:
            json.dump(task_data, f, indent=2)
    except Exception as e:
        print(f"Error writing updated task.json for task {task_id}: {e}")
        return

    # Clean up the old plan.md file
    os.remove(plan_path)
    print(f"  - Embedded plan into task.json and removed {plan_path}")


def main():
    """
    Main migration function.
    This script assumes a previous migration step has already created the
    `tasks/{id}/task.json` and `tasks/{id}/plan.md` files.
    This script's job is to embed the plan into the JSON and delete the markdown plan.
    """
    # Guard against running after TASKS.md is deleted in a later step.
    if not os.path.exists(TASKS_FILE):
        print("INFO: TASKS.md not found. Migration has likely already been completed.")
        return

    print("Starting plan embedding and cleanup phase of migration...")
    
    # Find all numeric task directories
    try:
        task_dirs = [d for d in os.listdir(TASKS_DIR) if os.path.isdir(os.path.join(TASKS_DIR, d)) and d.isdigit()]
    except FileNotFoundError:
        print(f"Error: Tasks directory '{TASKS_DIR}' not found.")
        sys.exit(1)

    for task_id_str in task_dirs:
        embed_plan_and_cleanup(task_id_str)

    print("Plan embedding and cleanup complete.")

if __name__ == "__main__":
    main()
