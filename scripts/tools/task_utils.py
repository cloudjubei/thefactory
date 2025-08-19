import os
import json
from typing import Dict, Any

def get_task(task_id: int, base_path: str = "tasks") -> Dict[str, Any] | None:
    """
    Reads a task from its JSON file.

    Args:
        task_id: The ID of the task to read.
        base_path: The base directory where tasks are stored.

    Returns:
        A dictionary representing the task, or None if not found.
    """
    task_file = os.path.join(base_path, str(task_id), "task.json")
    if not os.path.exists(task_file):
        return None
    try:
        with open(task_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except (IOError, json.JSONDecodeError):
        return None

def update_task(task_id: int, task_data: Dict[str, Any], base_path: str = "tasks") -> bool:
    """
    Updates an existing task's JSON file.

    Args:
        task_id: The ID of the task to update.
        task_data: A dictionary containing the updated task data.
        base_path: The base directory where tasks are stored.

    Returns:
        True if the update was successful, False otherwise.
    """
    task_dir = os.path.join(base_path, str(task_id))
    task_file = os.path.join(task_dir, "task.json")
    try:
        os.makedirs(task_dir, exist_ok=True)
        with open(task_file, "w", encoding="utf-8") as f:
            json.dump(task_data, f, indent=2)
        return True
    except IOError:
        return False

def create_task(task_data: Dict[str, Any], base_path: str = "tasks") -> Dict[str, Any] | None:
    """
    Creates a new task JSON file.

    Args:
        task_data: A dictionary containing the new task's data. Must include an 'id'.
        base_path: The base directory where tasks are stored.

    Returns:
        The created task data if successful, None otherwise.
    """
    task_id = task_data.get("id")
    if not task_id:
        return None
    
    task_dir = os.path.join(base_path, str(task_id))
    if os.path.exists(os.path.join(task_dir, "task.json")):
        return None # Task already exists

    if update_task(task_id, task_data, base_path):
        return task_data
    return None
