import os
import json
import re

def parse_plan_md(content: str) -> dict:
    """
    Parses plan.md content into a main plan and feature-specific plans.
    This is a simple parser assuming a certain structure where features are
    indicated by '### Feature {id}:' headings.
    """
    main_plan_parts = []
    feature_plans = {}
    current_feature_id = None

    lines = content.splitlines()
    for line in lines:
        feature_match = re.match(r'^###\s+Feature\s+([\d\.]+):', line)
        if feature_match:
            current_feature_id = feature_match.group(1)
            feature_plans[current_feature_id] = []
        elif current_feature_id:
            feature_plans[current_feature_id].append(line)
        else:
            main_plan_parts.append(line)

    plan_data = {
        "main": "\n".join(main_plan_parts).strip()
    }
    for fid, plan_lines in feature_plans.items():
        plan_data[fid] = "\n".join(plan_lines).strip()

    return plan_data

def embed_plans_in_json(base_dir: str = 'tasks'):
    """
    Finds all plan.md files, embeds their content into the corresponding
    task.json, and then deletes the plan.md file.
    """
    print("Starting plan embedding process...")
    if not os.path.isdir(base_dir):
        print(f"Error: Base directory '{base_dir}' not found.")
        return

    task_ids = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d)) and d.isdigit()]

    for task_id in task_ids:
        task_path = os.path.join(base_dir, task_id)
        plan_md_path = os.path.join(task_path, 'plan.md')
        task_json_path = os.path.join(task_path, 'task.json')

        if os.path.exists(plan_md_path) and os.path.exists(task_json_path):
            print(f"Processing task {task_id}...")
            try:
                with open(plan_md_path, 'r', encoding='utf-8') as f:
                    plan_content = f.read()

                with open(task_json_path, 'r', encoding='utf-8') as f:
                    task_data = json.load(f)

                parsed_plans = parse_plan_md(plan_content)

                task_data['plan'] = parsed_plans.get('main', '')

                if 'features' in task_data and isinstance(task_data['features'], list):
                    for feature in task_data['features']:
                        feature_id = feature.get('id')
                        if feature_id in parsed_plans:
                            feature['plan'] = parsed_plans[feature_id]

                with open(task_json_path, 'w', encoding='utf-8') as f:
                    json.dump(task_data, f, indent=2)
                    f.write('\n') # Add trailing newline

                os.remove(plan_md_path)
                print(f"  - Successfully embedded plan.md and removed the file for task {task_id}.")

            except Exception as e:
                print(f"  - ERROR processing task {task_id}: {e}")

if __name__ == "__main__":
    embed_plans_in_json()
    print("\nPlan embedding complete.")
