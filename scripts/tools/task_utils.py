from __future__ import annotations
import json
import os
from typing import Any, Optional, Tuple, List, cast

# Use the canonical schema types
try:
    from docs.tasks.task_format import Task, Feature
except Exception:
    # Fallback to loose typing if schema import fails at runtime
    Task = dict  # type: ignore
    Feature = dict  # type: ignore


def _task_path(task_id: int, base_path: str = "tasks") -> str:
    """Return the absolute path to a task.json file under tasks/{task_id}/.

    Args:
        task_id: The numeric task ID.
        base_path: Root folder for tasks (default: "tasks").
    Returns:
        The filesystem path to tasks/{task_id}/task.json.
    """
    return os.path.join(base_path, str(task_id), "task.json")


def _ensure_task_dir(task_id: int, base_path: str = "tasks") -> str:
    """Ensure the directory tasks/{task_id}/ exists and return its path."""
    task_dir = os.path.join(base_path, str(task_id))
    os.makedirs(task_dir, exist_ok=True)
    return task_dir


def _read_json(path: str) -> dict:
    """Read a JSON file and return its contents.

    Raises:
        FileNotFoundError: if the file does not exist.
        ValueError: if the file cannot be parsed as JSON.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Task file does not exist: {path}")
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON at {path}: {e}")


def _write_json(path: str, data: dict) -> None:
    """Write a JSON file with UTF-8 encoding and pretty formatting."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


# Public API

def get_task(task_id: int, base_path: str = "tasks") -> Task | None:
    """Load and return a Task by ID.

    Args:
        task_id: Numeric task ID.
        base_path: Root folder for tasks.
    Returns:
        The Task dict if found, else None.
    """
    path = _task_path(task_id, base_path)
    try:
        data = _read_json(path)
        return cast(Task, data)
    except FileNotFoundError:
        return None
    except ValueError:
        # Malformed JSON
        return None


def update_task(task_id: int, task_data: Task, base_path: str = "tasks") -> None:
    """Persist the provided Task data to tasks/{task_id}/task.json.

    Args:
        task_id: Numeric task ID.
        task_data: The full Task object to write.
        base_path: Root folder for tasks.
    Raises:
        ValueError: if task_data.id does not match task_id.
    """
    if isinstance(task_data, dict) and str(task_data.get("id")) != str(task_id):
        raise ValueError("update_task: task_data.id does not match task_id")
    _ensure_task_dir(task_id, base_path)
    _write_json(_task_path(task_id, base_path), cast(dict, task_data))


def create_task(
    task_id: int,
    title: str,
    action: str,
    *,
    features: Optional[List[Feature]] = None,
    status: str = "-",
    plan: str = "",
    acceptance: Optional[list] = None,
    base_path: str = "tasks",
) -> Task:
    """Create a new task at tasks/{task_id}/task.json.

    If the file already exists, it will be overwritten.

    Args:
        task_id: Numeric task ID.
        title: Task title.
        action: High-level action/goal.
        features: Optional list of Feature dicts.
        status: Task status flag ("-", "~", "+", etc.).
        plan: Optional human-readable plan string.
        acceptance: Optional acceptance structure (list or nested dicts).
        base_path: Root folder for tasks.
    Returns:
        The created Task object.
    """
    _ensure_task_dir(task_id, base_path)
    task: Task = cast(Task, {
        "id": task_id,
        "status": status,
        "title": title,
        "action": action,
        "plan": plan,
        "acceptance": acceptance or [],
        "features": features or [],
    })
    _write_json(_task_path(task_id, base_path), cast(dict, task))
    return task


def get_feature(task: Task, feature_number: int) -> Tuple[int, Feature]:
    """Retrieve a feature by its ordinal number (e.g., 4 for feature '13.4').

    Args:
        task: Task object.
        feature_number: Ordinal feature number within the task.
    Returns:
        (index, Feature) where index is the position in the features list.
    Raises:
        IndexError: if the feature cannot be found.
    """
    features = cast(List[Feature], task.get("features", []))
    # Match by suffix number or by positional index if ids are consistent
    for i, feat in enumerate(features):
        fid = str(feat.get("id", ""))
        # Support ids like "13.4" or just "4"
        if fid.endswith(f".{feature_number}") or fid == str(feature_number):
            return i, cast(Feature, feat)
    # Fallback: treat feature_number as 1-based index
    idx = feature_number - 1
    if 0 <= idx < len(features):
        return idx, cast(Feature, features[idx])
    raise IndexError(f"Feature {feature_number} not found in task {task.get('id')}")


def update_feature(task: Task, feature_number: int, new_feature: Feature) -> Task:
    """Replace a feature in the task by feature number and return the updated task."""
    idx, _ = get_feature(task, feature_number)
    features = cast(List[Feature], task.get("features", []))
    features[idx] = new_feature
    task["features"] = features
    return task


def update_task_status(task_id: int, status: str, *, base_path: str = "tasks") -> Task:
    """Update a task's status and persist the change.

    Args:
        task_id: Task ID.
        status: New status symbol.
        base_path: Root folder for tasks.
    Returns:
        The updated Task object.
    Raises:
        FileNotFoundError: if the task does not exist.
    """
    task = get_task(task_id, base_path)
    if task is None:
        raise FileNotFoundError(f"Task {task_id} not found")
    task["status"] = status
    update_task(task_id, task, base_path)
    return task


def update_feature_status(task_id: int, feature_number: int, status: str, *, base_path: str = "tasks") -> Task:
    """Update the status of a specific feature and persist the change.

    Args:
        task_id: Task ID.
        feature_number: Ordinal number within the task (e.g., 4 for '13.4').
        status: New status symbol.
        base_path: Root folder for tasks.
    Returns:
        The updated Task object.
    Raises:
        FileNotFoundError: if the task does not exist.
        IndexError: if the feature cannot be found.
    """
    task = get_task(task_id, base_path)
    if task is None:
        raise FileNotFoundError(f"Task {task_id} not found")
    idx, feat = get_feature(task, feature_number)
    feat = cast(Feature, {**feat, "status": status})
    task = update_feature(task, feature_number, feat)
    update_task(task_id, task, base_path)
    return task


def ask_agent_question(task_id: int, question_text: str, *, feature_number: Optional[int] = None, base_path: str = "tasks") -> Task:
    """Set or update the agent_question field on a task or a specific feature.

    This function is intended to replace prior ad-hoc ask_question tooling that
    required direct text editing. It ensures questions are encoded in JSON.

    Args:
        task_id: Task ID.
        question_text: The question to persist.
        feature_number: If provided, set the question on that feature; otherwise on the task.
        base_path: Root folder for tasks.
    Returns:
        The updated Task object with the question persisted.
    Raises:
        FileNotFoundError: if the task or feature is missing.
    """
    task = get_task(task_id, base_path)
    if task is None:
        raise FileNotFoundError(f"Task {task_id} not found")

    if feature_number is None:
        task["agent_question"] = question_text
    else:
        idx, feat = get_feature(task, feature_number)
        feat = cast(Feature, {**feat, "agent_question": question_text})
        task = update_feature(task, feature_number, feat)

    update_task(task_id, task, base_path)
    return task
