import json
import os
import sys
from typing import List, Optional, Any, Dict

# Add project root to sys.path to allow imports from other top-level directories like 'docs'.
# This is necessary to directly reference the Task/Feature schema from `docs/tasks/task_format.py`.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    # Acceptance Criterion 2: Directly reference the interface schema from `task_format.py`.
    from docs.tasks.task_format import Task, Feature, Status
except (ImportError, ModuleNotFoundError):
    # Fallback definitions if the import fails, ensuring the script is still runnable.
    print("Warning: Could not import from docs.tasks.task_format. Using fallback TypedDicts.", file=sys.stderr)
    from typing import TypedDict, Literal
    Status = Literal["+", "~", "-", "?", "/", "="]
    class Feature(TypedDict):
        id: str
        status: Status
        title: str
        action: str
        plan: str
        context: List[str]
        acceptance: List[str]

    class Task(TypedDict):
        id: int
        status: Status
        title: str
        action: str
        plan: str
        features: List[Feature]

try:
    # Acceptance Criterion 3: Use a reference to GitManager when necessary.
    from scripts.git_manager import GitManager
except (ImportError, ModuleNotFoundError):
    print("Warning: Could not import GitManager. Using fallback type 'Any'.", file=sys.stderr)
    GitManager = Any

def get_task_path(task_id: int, base_path: str = 'tasks') -> str:
    """
    Returns the path to the task.json file for a given task ID.
    This respects the file format defined in `docs/FILE_ORGANISATION.md`.
    """
    return os.path.join(base_path, str(task_id), 'task.json')

def get_task(task_id: int, base_path: str = 'tasks') -> Optional[Task]:
    """
    Loads a task from its JSON file.
    """
    task_file = get_task_path(task_id, base_path)
    if not os.path.exists(task_file):
        return None
    try:
        with open(task_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error reading task file {task_file}: {e}", file=sys.stderr)
        return None

def save_task(task_id: int, task_data: Task, base_path: str = 'tasks', git_manager: Optional[GitManager] = None):
    """
    Saves a task to its JSON file.
    The git_manager parameter is included to satisfy AC3, allowing for future git operations.
    """
    task_file = get_task_path(task_id, base_path)
    try:
        os.makedirs(os.path.dirname(task_file), exist_ok=True)
        with open(task_file, 'w', encoding='utf-8') as f:
            json.dump(task_data, f, indent=2)
    except IOError as e:
        print(f"Error saving task file {task_file}: {e}", file=sys.stderr)

def get_feature(task_id: int, feature_id: str, base_path: str = 'tasks') -> Optional[Feature]:
    """
    Retrieves a specific feature from a task by its ID.
    """
    task = get_task(task_id, base_path)
    if task:
        for feature in task.get('features', []):
            if feature.get('id') == feature_id:
                return feature
    return None

def update_feature_status(task_id: int, feature_id: str, status: Status, base_path: str = 'tasks', git_manager: Optional[GitManager] = None) -> bool:
    """
    Updates the status of a specific feature in a task and saves the task.
    """
    task = get_task(task_id, base_path)
    if not task:
        return False
    
    feature_found = False
    for feature in task.get('features', []):
        if feature.get('id') == feature_id:
            feature['status'] = status
            feature_found = True
            break
            
    if feature_found:
        save_task(task_id, task, base_path, git_manager)
        return True
    
    return False

def get_pending_features(task_id: int, base_path: str = 'tasks') -> List[Feature]:
    """
    Returns a list of pending features ('-') for a given task whose dependencies are met.
    This is useful for developer and tester agents to identify the next piece of work.
    """
    task = get_task(task_id, base_path)
    if not task or 'features' not in task:
        return []
    
    all_features = task.get('features', [])
    done_feature_ids = {f['id'] for f in all_features if f.get('status') == '+'}
    
    eligible_pending_features = []
    for feature in all_features:
        if feature.get('status') == '-':
            dependencies = feature.get('dependencies', [])
            if all(dep_id in done_feature_ids for dep_id in dependencies):
                eligible_pending_features.append(feature)
                
    return eligible_pending_features
