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
    Reads a task from its JSON file. This is the single source of truth.
    It does not read or merge plan.md files.
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
