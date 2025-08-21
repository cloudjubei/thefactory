import os
import json
from .task_utils import move_task_logic

def move_task_tool(task_id: int, new_index: int, repo_path: str):
    """
    Tool to move a task to a different position in the list of tasks.
    It renames task directories and updates all task IDs and feature dependencies accordingly.
    """
    tasks_dir = os.path.join(repo_path, 'tasks')
    result = move_task_logic(task_id, new_index, tasks_dir)
    return json.dumps(result)
