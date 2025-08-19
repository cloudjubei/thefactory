import os
import re
import json
import shutil

def parse_features_from_plan(plan_content: str) -> list:
    """Parses features from the content of a plan.md file."""
    features = []
    # Regex to find feature blocks starting with e.g. "13.1) -"
    feature_blocks = re.split(r'\n(?=\d+\.\d+\))', plan_content)

    for block in feature_blocks:
        block = block.strip()
        if not block:
            continue
        
        header_match = re.search(r'^(?P<id>\d+\.\d+)\)\s+(?P<status>[+\-~?/])\s+(?P<title>.*)', block)
        if not header_match:
            continue

        feature_dict = header_match.groupdict()
        feature = {
            'id': feature_dict['id'].strip(),
            'status': feature_dict['status'].strip(),
            'title': feature_dict['title'].strip(),
            'action': '',
            'acceptance': ''
        }
        
        action_match = re.search(r'Action:\s*((.|
)*?)(?=\n\s*Acceptance:|\n\s*Dependencies:|\Z)', block, re.DOTALL)
        if action_match:
            feature['action'] = action_match.group(1).strip()
            
        acceptance_match = re.search(r'Acceptance:\s*((.|
)*?)(?=\n\s*Dependencies:|\n\s*Output:|\Z)', block, re.DOTALL)
        if acceptance_match:
            feature['acceptance'] = acceptance_match.group(1).strip()

        features.append(feature)
    return features

def migrate():
    """Main migration function."""
    tasks_md_path = os.path.join('tasks', 'TASKS.md')
    if not os.path.exists(tasks_md_path):
        print(f"Error: {tasks_md_path} not found.")
        return

    print("Reading TASKS.md...")
    with open(tasks_md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    task_blocks = re.split(r'\n(?=\d+\)\s+[+\-~?])', content)
    
    for block in task_blocks[1:]:
        block = block.strip()
        header_match = re.match(r'(?P<id>\d+)\)\s+(?P<status>[+\-~?])\s+(?P<title>.*)', block)
        if not header_match:
            continue
            
        task_dict = header_match.groupdict()
        task_id = int(task_dict['id'])
        print(f"Processing Task {task_id}: {task_dict['title']}")
        
        action_match = re.search(r'Action:((.|
)*?)Acceptance:', block, re.DOTALL)
        action = action_match.group(1).strip() if action_match else ''
        
        acceptance_match = re.search(r'Acceptance:((.|
)*)', block, re.DOTALL)
        acceptance_str = acceptance_match.group(1).strip() if acceptance_match else ''
        
        task_data = {
            'id': task_id,
            'title': task_dict['title'].strip(),
            'status': task_dict['status'].strip(),
            'action': action,
            'acceptance': acceptance_str,
            'features': []
        }

        old_plan_path = os.path.join('tasks', str(task_id), f'plan_{task_id}.md')
        new_plan_path = os.path.join('tasks', str(task_id), 'plan.md')

        if os.path.exists(old_plan_path):
            with open(old_plan_path, 'r', encoding='utf-8') as f:
                plan_content = f.read()
            task_data['features'] = parse_features_from_plan(plan_content)
            print(f"  - Parsed {len(task_data['features'])} features from plan.")
        
        task_json_path = os.path.join('tasks', str(task_id), 'task.json')
        os.makedirs(os.path.dirname(task_json_path), exist_ok=True)
        with open(task_json_path, 'w', encoding='utf-8') as f:
            json.dump(task_data, f, indent=2)
        print(f"  - Created {task_json_path}")
        
        if os.path.exists(old_plan_path):
            shutil.move(old_plan_path, new_plan_path)
            print(f"  - Renamed {old_plan_path} to {new_plan_path}")
            
    print("\nMigration script completed.")

if __name__ == '__main__':
    migrate()
