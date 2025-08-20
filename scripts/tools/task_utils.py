import os
import json
from typing import Any, TypedDict, Optional

# Base directory for tasks
TASKS_BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'tasks')

class TaskNotFoundError(Exception):
    pass

class FeatureNotFoundError(Exception):
    pass


def _task_path(task_id: int, base_path: Optional[str] = None) -> str:
    base = base_path or TASKS_BASE_DIR
    return os.path.join(base, str(task_id), 'task.json')


def get_task(task_id: int, base_path: Optional[str] = None) -> Optional[dict]:
    """Read a task JSON file and return its data or None if not found."""
    path = _task_path(task_id, base_path)
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_task(task_id: int, task_data: dict, base_path: Optional[str] = None) -> None:
    """Persist a task JSON file atomically."""
    path = _task_path(task_id, base_path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp_path = path + '.tmp'
    with open(tmp_path, 'w', encoding='utf-8') as f:
        json.dump(task_data, f, indent=2, ensure_ascii=False)
        f.write('\n')
    os.replace(tmp_path, path)


def update_feature_status(task_id: int, feature_number: int, new_status: str, reason: str = "", base_path: Optional[str] = None) -> str:
    """
    Update the status of a specific feature within tasks/{task_id}/task.json.

    Args:
        task_id: The numeric ID of the task (e.g., 13).
        feature_number: The feature index (e.g., for 13.9 pass 9).
        new_status: One of '+', '~', '-', '?', '/', '='.
        reason: Optional note explaining the status change.
        base_path: Optional override base tasks path (used by orchestrator/tests).

    Returns:
        A JSON string with keys: ok (bool), message (str), previous_status (str).
    """
    allowed = ['+', '~', '-', '?', '/', '=']
    if new_status not in allowed:
        return json.dumps({
            'ok': False,
            'message': f"Invalid status '{new_status}'. Allowed: {allowed}",
            'previous_status': ''
        })

    task = get_task(task_id, base_path=base_path)
    if task is None:
        return json.dumps({'ok': False, 'message': f'Task {task_id} not found.', 'previous_status': ''})

    features = task.get('features') or []
    idx = None
    for i, feat in enumerate(features):
        # Feature IDs may be strings like '13.9' or numbers
        fid = str(feat.get('id'))
        if fid.endswith(f'.{feature_number}') or fid == f"{task_id}.{feature_number}":
            idx = i
            break
    if idx is None:
        return json.dumps({'ok': False, 'message': f'Feature {task_id}.{feature_number} not found.', 'previous_status': ''})

    prev = features[idx].get('status', '')
    features[idx]['status'] = new_status
    if reason:
        # record lightweight audit trail in feature object
        notes = features[idx].get('notes')
        audit_line = f"Status changed to '{new_status}'"
        if reason:
            audit_line += f": {reason}"
        if notes:
            features[idx]['notes'] = f"{notes}\n{audit_line}"
        else:
            features[idx]['notes'] = audit_line

    # Persist
    task['features'] = features
    save_task(task_id, task, base_path=base_path)

    return json.dumps({'ok': True, 'message': 'Feature status updated.', 'previous_status': prev})


def create_task(task_data: dict, base_path: Optional[str] = None) -> str:
    """Create a new task with the provided data structure."""
    task_id = task_data.get('id')
    if task_id is None:
        return json.dumps({'ok': False, 'message': 'Task data missing id.'})
    path = _task_path(task_id, base_path)
    if os.path.exists(path):
        return json.dumps({'ok': False, 'message': f'Task {task_id} already exists.'})
    save_task(task_id, task_data, base_path=base_path)
    return json.dumps({'ok': True, 'message': f'Task {task_id} created.'})


def update_task(task_id: int, task_data: dict, base_path: Optional[str] = None) -> str:
    """Overwrite the entire task definition with provided data."""
    if get_task(task_id, base_path=base_path) is None:
        return json.dumps({'ok': False, 'message': f'Task {task_id} not found.'})
    save_task(task_id, task_data, base_path=base_path)
    return json.dumps({'ok': True, 'message': f'Task {task_id} updated.'})
