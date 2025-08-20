import os
import json
import errno
import importlib.util
from typing import Any, Dict, Optional

# Load canonical types from docs/tasks/task_format.py even if 'docs' is not a package

def _load_task_format_module():
    """Dynamically load docs/tasks/task_format.py as a module and return it.
    This allows us to reference the canonical Task/Feature/Status types directly
    even if 'docs' isn't a Python package.
    """
    here = os.path.abspath(os.path.dirname(__file__))
    repo_root = os.path.abspath(os.path.join(here, "..", ".."))
    tf_path = os.path.join(repo_root, "docs", "tasks", "task_format.py")
    spec = importlib.util.spec_from_file_location("task_format", tf_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load task_format module from {tf_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[attr-defined]
    return module

try:
    # Try normal import first in case docs is a package in this environment
    from docs.tasks.task_format import Task as _Task, Feature as _Feature, Status as _Status  # type: ignore
except Exception:
    # Fallback to dynamic import
    _tf = _load_task_format_module()
    _Task = _tf.Task
    _Feature = _tf.Feature
    _Status = _tf.Status

# Re-export canonical types for visibility and testability
Task = _Task
Feature = _Feature
Status = _Status

__all__ = [
    "Task",
    "Feature",
    "Status",
    "get_task",
    "update_task",
    "create_task",
    "update_task_status",
    "update_feature_status",
    "ask_agent_question",
]


def _task_dir(task_id: int, base_path: str) -> str:
    return os.path.join(base_path, str(task_id))


def _task_path(task_id: int, base_path: str) -> str:
    return os.path.join(_task_dir(task_id, base_path), "task.json")


def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def _read_json(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: str, data: Dict[str, Any]) -> None:
    _ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def get_task(task_id: int, base_path: str = "tasks") -> Task:
    """Return the task data for the given task_id from base_path.

    Args:
        task_id: The task numeric identifier.
        base_path: The base directory containing task folders.
    Returns:
        Task: The parsed task object.
    """
    path = _task_path(task_id, base_path)
    data = _read_json(path)
    return data  # type: ignore[return-value]


def update_task(task_id: int, task_data: Task, base_path: str = "tasks") -> Task:
    """Update the entire task.json for a given task_id with provided task_data.

    Raises if the task directory does not exist.
    """
    path = _task_path(task_id, base_path)
    if not os.path.isdir(os.path.dirname(path)):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), os.path.dirname(path))
    _write_json(path, task_data)
    # Re-read to return the canonical on-disk representation
    return get_task(task_id, base_path=base_path)


def create_task(task_data: Task, base_path: str = "tasks") -> Task:
    """Create a new task directory and task.json from the given task_data.

    The task id is taken from task_data["id"]. It can be a string or int-like; it
    will be used for the folder name as-is.
    """
    task_id_raw = task_data.get("id")
    if task_id_raw is None:
        raise ValueError("task_data must include an 'id' field")
    task_id_str = str(task_id_raw)
    # We still accept an int 'task_id' arg in other functions; here we derive folder from task_data
    path = _task_path(int(task_id_str) if task_id_str.isdigit() else task_id_str, base_path)  # type: ignore[arg-type]
    if os.path.exists(path):
        raise FileExistsError(errno.EEXIST, os.strerror(errno.EEXIST), path)
    _write_json(path, task_data)
    # Return what was written
    if task_id_str.isdigit():
        return get_task(int(task_id_str), base_path=base_path)
    else:
        # Non-numeric id fallback: read directly
        return _read_json(path)  # type: ignore[return-value]


def update_task_status(task_id: int, status: Status, base_path: str = "tasks") -> Task:
    """Update the top-level status field for a task and persist the change."""
    task = get_task(task_id, base_path=base_path)
    task["status"] = status  # type: ignore[index]
    return update_task(task_id, task, base_path=base_path)


def update_feature_status(task_id: int, feature_id: int, status: Status, base_path: str = "tasks") -> Feature:
    """Update status of a specific feature (by numeric feature_id) within a task.

    Returns the updated Feature object.
    """
    task = get_task(task_id, base_path=base_path)
    features = task.get("features", [])  # type: ignore[assignment]
    feature_key = f"{task_id}.{feature_id}"
    target_index: Optional[int] = None
    for i, feat in enumerate(features):
        if isinstance(feat, dict) and feat.get("id") == feature_key:
            target_index = i
            break
    if target_index is None:
        # Try a fallback: match by suffix after '.' in case of string vs int id mismatches
        for i, feat in enumerate(features):
            fid = str(feat.get("id", ""))
            if fid.split(".")[-1] == str(feature_id):
                target_index = i
                break
    if target_index is None:
        raise KeyError(f"Feature {feature_key} not found in task {task_id}")

    features[target_index]["status"] = status  # type: ignore[index]
    update_task(task_id, task, base_path=base_path)
    return features[target_index]  # type: ignore[return-value]


def ask_agent_question(task_id: int, feature_id: Optional[int], question: str, base_path: str = "tasks") -> Task:
    """Edit the task's or feature's `agent_question` field.

    If feature_id is None, set task-level agent_question; otherwise set it on the
    specified feature. This function supersedes older ask_question tooling.
    """
    task = get_task(task_id, base_path=base_path)
    if feature_id is None:
        task["agent_question"] = question  # type: ignore[index]
    else:
        features = task.get("features", [])  # type: ignore[assignment]
        feature_key = f"{task_id}.{feature_id}"
        target: Optional[Dict[str, Any]] = None
        for feat in features:
            if isinstance(feat, dict) and feat.get("id") == feature_key:
                target = feat
                break
        if target is None:
            # Fallback: match by numeric suffix
            for feat in features:
                fid = str(feat.get("id", ""))
                if fid.split(".")[-1] == str(feature_id):
                    target = feat
                    break
        if target is None:
            raise KeyError(f"Feature {feature_key} not found in task {task_id}")
        target["agent_question"] = question
    return update_task(task_id, task, base_path=base_path)
