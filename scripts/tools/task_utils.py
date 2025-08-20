import json
import os
from typing import Dict, Any

def get_task(task_id: int, base_path: str = 'tasks') -> Dict[str, Any] | None:
    """
    Retrieves a task dictionary from its JSON file.
    """
    task_file = os.path.join(base_path, str(task_id), 'task.json')
    if not os.path.exists(task_file):
        return None
    try:
        with open(task_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (IOError, json.JSONDecodeError):
        return None

def update_task(task_id: int, task_data: Dict[str, Any], base_path: str = 'tasks') -> bool:
    """
    Updates a task's JSON file with new data.
    """
    task_dir = os.path.join(base_path, str(task_id))
    if not os.path.exists(task_dir):
        return False
    task_file = os.path.join(task_dir, 'task.json')
    try:
        with open(task_file, 'w', encoding='utf-8') as f:
            json.dump(task_data, f, indent=2)
        return True
    except IOError:
        return False

def create_task(task_id: int, task_data: Dict[str, Any], base_path: str = 'tasks') -> bool:
    """
    Creates a new task directory and JSON file.
    """
    task_dir = os.path.join(base_path, str(task_id))
    if os.path.exists(task_dir):
        return False
    try:
        os.makedirs(task_dir)
        return update_task(task_id, task_data, base_path)
    except OSError:
        return False
