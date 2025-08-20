import json
import os
from typing import TypedDict, List, Optional

class Feature(TypedDict):
    id: str
    status: str
    title: str
    action: str
    acceptance: List[str]
    dependencies: Optional[List[str]]
    output: Optional[str]
    plan: Optional[str]

class AcceptancePhase(TypedDict):
    phase: str
    criteria: List[str]

class Task(TypedDict):
    id: int
    status: str
    title: str
    action: str
    plan: str
    acceptance: List[AcceptancePhase]
    features: List[Feature]

def get_task(task_id: int, base_path: str = 'tasks') -> Optional[Task]:
    """
    Reads a task from its JSON file.
    """
    task_file = os.path.join(base_path, str(task_id), 'task.json')
    if not os.path.exists(task_file):
        return None
    try:
        with open(task_file, 'r', encoding='utf-8') as f:
            task_data: Task = json.load(f)
        return task_data
    except (json.JSONDecodeError, IOError):
        return None

def update_task(task_data: Task, base_path: str = 'tasks') -> bool:
    """Saves a task to its JSON file. Alias for save_task for backward compatibility.
    """
    task_id = task_data.get('id')
    if not task_id:
        return False
    task_dir = os.path.join(base_path, str(task_id))
    if not os.path.exists(task_dir):
        os.makedirs(task_dir)
    task_file = os.path.join(task_dir, 'task.json')
    try:
        with open(task_file, 'w', encoding='utf-8') as f:
            json.dump(task_data, f, indent=2)
            f.write('\n')
        return True
    except IOError:
        return False

def create_task(task_data: Task, base_path: str = 'tasks') -> bool:
    """Creates a new task directory and task.json file."""
    return update_task(task_data, base_path)

def update_feature_status(task_id: int, feature_number: int, new_status: str, base_path: str = 'tasks') -> dict:
    """Updates the status of a specific feature in a task's JSON file."""
    task_data = get_task(task_id, base_path=base_path)
    if not task_data:
        return {"ok": False, "error": f"Task {task_id} not found."}

    feature_id_to_find = f"{task_id}.{feature_number}"
    feature_found = False
    previous_status = None

    if 'features' in task_data:
        for feature in task_data['features']:
            if feature.get('id') == feature_id_to_find:
                previous_status = feature.get('status')
                feature['status'] = new_status
                feature_found = True
                break

    if not feature_found:
        return {"ok": False, "error": f"Feature {feature_id_to_find} not found in task {task_id}."}

    if update_task(task_data, base_path=base_path):
        return {
            "ok": True,
            "message": f"Successfully updated feature {feature_id_to_find} to status '{new_status}'.",
            "previous_status": previous_status
        }
    else:
        return {"ok": False, "error": f"Failed to save updated task {task_id}."}
