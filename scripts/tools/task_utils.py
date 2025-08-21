import json
import os
import sys
from pathlib import Path
from typing import Optional

# To reference docs.tasks.task_format, we need to add the project root to sys.path
# as 'docs' is not a package.
# Assuming this script is at <project_root>/scripts/tools/task_utils.py
# The project root is two levels up.
project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from docs.tasks.task_format import Task, Feature, Status

TASKS_DIR = "tasks"

def get_task(task_id: int, base_path: str = TASKS_DIR) -> Optional[Task]:
    """Reads a task from its JSON file."""
    task_file = Path(base_path) / str(task_id) / "task.json"
    if not task_file.exists():
        return None
    with open(task_file, "r", encoding="utf-8") as f:
        return json.load(f)

def create_task(task: Task, base_path: str = TASKS_DIR) -> bool:
    """Creates a new task directory and task.json file."""
    task_dir = Path(base_path) / str(task['id'])
    task_file = task_dir / "task.json"
    if task_file.exists():
        print(f"Error: Task {task['id']} already exists at {task_file}")
        return False
    task_dir.mkdir(parents=True, exist_ok=True)
    with open(task_file, "w", encoding="utf-8") as f:
        json.dump(task, f, indent=2)
    return True

def update_task(task: Task, base_path: str = TASKS_DIR) -> bool:
    """Updates an existing task.json file."""
    task_file = Path(base_path) / str(task['id']) / "task.json"
    if not task_file.exists():
        print(f"Error: Task {task['id']} does not exist at {task_file}")
        return False
    with open(task_file, "w", encoding="utf-8") as f:
        json.dump(task, f, indent=2)
    return True

def move_task(old_task_id: int, new_task_id: int, base_path: str = TASKS_DIR) -> bool:
    """Renames a task directory and updates the task ID within its JSON file."""
    old_task_dir = Path(base_path) / str(old_task_id)
    new_task_dir = Path(base_path) / str(new_task_id)
    if not old_task_dir.exists():
        print(f"Error: Source task {old_task_id} does not exist.")
        return False
    if new_task_dir.exists():
        print(f"Error: Target task directory {new_task_id} already exists.")
        return False
    
    old_task_dir.rename(new_task_dir)
    
    task = get_task(new_task_id, base_path=str(new_task_dir.parent))
    if task:
        task['id'] = new_task_id
        for feature in task.get('features', []):
            try:
                parts = feature['id'].split('.')
                if len(parts) == 2:
                    feature['id'] = f"{new_task_id}.{parts[1]}"
            except (AttributeError, IndexError):
                pass
        return update_task(task, base_path=str(new_task_dir.parent))
    return False

def update_task_status(task_id: int, status: Status, base_path: str = TASKS_DIR) -> bool:
    """Updates the status of a specific task."""
    task = get_task(task_id, base_path)
    if not task:
        return False
    task['status'] = status
    return update_task(task, base_path)

def update_feature_status(task_id: int, feature_id: str, status: Status, base_path: str = TASKS_DIR) -> bool:
    """Updates the status of a specific feature within a task."""
    task = get_task(task_id, base_path)
    if not task:
        return False
    
    feature_found = False
    for feature in task.get('features', []):
        if feature.get('id') == feature_id:
            feature['status'] = status
            feature_found = True
            break
            
    if not feature_found:
        print(f"Error: Feature {feature_id} not found in task {task_id}.")
        return False
        
    return update_task(task, base_path)

def set_agent_question(task_id: int, feature_id: str, question: str, base_path: str = TASKS_DIR) -> bool:
    """Sets the agent_question for a specific feature."""
    task = get_task(task_id, base_path)
    if not task:
        return False
        
    feature_found = False
    for feature in task.get('features', []):
        if feature.get('id') == feature_id:
            feature['agent_question'] = question
            feature_found = True
            break
            
    if not feature_found:
        print(f"Error: Feature {feature_id} not found in task {task_id}.")
        return False
        
    return update_task(task, base_path)
