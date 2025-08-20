"""
Task utilities for JSON-based tasks.

This module provides helpers to read, create, and update tasks and features stored as JSON
in tasks/{task_id}/task.json and is the single point for task I/O.

It references the canonical schema defined in docs/tasks/task_format.py for Task, Feature, and Status.
"""
from __future__ import annotations

import os
import json
from typing import Optional, cast

# Reference the canonical schema directly; fall back gracefully if import-time packages are not configured.
try:
    from docs.tasks.task_format import Task, Feature, Status  # type: ignore
except Exception:  # pragma: no cover - fallback for environments without package imports
    from typing import TypedDict, List, Literal  # type: ignore

    Status = Literal["+", "~", "-", "?", "/", "="]

    class Feature(TypedDict, total=False):
        id: str
        status: Status
        title: str
        action: str
        plan: str
        context: List[str]
        acceptance: List[str]
        dependencies: List[str]
        rejection: str
        agent_question: str

    class Task(TypedDict):
        id: str
        status: Status
        title: str
        action: str
        plan: str
        features: List[Feature]


__all__ = [
    "get_task",
    "update_task",
    "create_task",
    "update_task_status",
    "update_feature_status",
    "ask_agent_question",
]


def _task_json_path(task_id: int, base_path: str = "tasks") -> str:
    return os.path.join(base_path, str(task_id), "task.json")


def _read_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: str, data: dict) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def _load_task(task_id: int, base_path: str) -> Task:
    path = _task_json_path(task_id, base_path)
    data = _read_json(path)
    return cast(Task, data)


def _save_task(task_id: int, task_data: Task, base_path: str) -> Task:
    path = _task_json_path(task_id, base_path)
    _write_json(path, task_data)
    return task_data


def _find_feature(task: Task, task_id: int, feature_id: int) -> Feature:
    id_str = str(task.get("id", task_id))
    candidates = task.get("features", [])
    target_suffix = str(feature_id)
    for feat in candidates:
        fid = str(feat.get("id", ""))
        # Match either exact "{task_id}.{feature_id}" or suffix match on ".{feature_id}"
        if fid == f"{id_str}.{target_suffix}" or fid.split(".")[-1] == target_suffix:
            return feat
    raise ValueError(f"Feature {task_id}.{feature_id} not found in task {id_str}.")


# Public API

def get_task(task_id: int, base_path: str = "tasks") -> Task:
    """Return the Task object for the given task_id."""
    return _load_task(task_id, base_path)


def update_task(task_id: int, task_data: Task, base_path: str = "tasks") -> Task:
    """Overwrite the task.json for task_id with task_data and return the updated Task."""
    return _save_task(task_id, task_data, base_path)


def create_task(task_data: Task, base_path: str = "tasks") -> Task:
    """Create a new task folder and task.json from the provided Task data and return it.

    Also ensures a tests/ directory exists under the task folder.
    """
    # Accept id as int or str from provided data
    tid_raw = task_data.get("id")
    if tid_raw is None:
        raise ValueError("task_data must include an 'id' field")
    try:
        task_id = int(tid_raw)  # normalize to int for path building
    except Exception:
        # If id is non-numeric, keep as string for folder naming
        # but attempt int conversion for feature matching only.
        task_id = int(str(tid_raw)) if str(tid_raw).isdigit() else str(tid_raw)  # type: ignore

    folder = os.path.join(base_path, str(task_id))
    os.makedirs(folder, exist_ok=True)
    os.makedirs(os.path.join(folder, "tests"), exist_ok=True)

    path = _task_json_path(int(task_id) if isinstance(task_id, int) else int(str(task_id)), base_path) if str(task_id).isdigit() else os.path.join(folder, "task.json")
    _write_json(path, task_data)
    return task_data


def update_task_status(task_id: int, status: Status, base_path: str = "tasks") -> Task:
    """Update a task's status and persist the change."""
    task = _load_task(task_id, base_path)
    task["status"] = cast(str, status)
    return _save_task(task_id, task, base_path)


def update_feature_status(task_id: int, feature_id: int, status: Status, base_path: str = "tasks") -> Feature:
    """Update a feature's status and persist the change. Returns the updated Feature."""
    task = _load_task(task_id, base_path)
    feat = _find_feature(task, task_id, feature_id)
    feat["status"] = cast(str, status)
    _save_task(task_id, task, base_path)
    return feat


def ask_agent_question(task_id: int, question: str, feature_id: Optional[int] = None, base_path: str = "tasks") -> Task:
    """Edit the agent_question field on the task or a specific feature and persist it.

    If feature_id is provided, the question is set on that feature; otherwise it is set on the task.
    Returns the updated Task.
    """
    task = _load_task(task_id, base_path)
    if feature_id is None:
        # place at the task level
        task["agent_question"] = question  # type: ignore[assignment]
    else:
        feat = _find_feature(task, task_id, feature_id)
        feat["agent_question"] = question
    return _save_task(task_id, task, base_path)
