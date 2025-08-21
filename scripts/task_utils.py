from __future__ import annotations
"""Utility helpers for safely manipulating task definition files (tasks/{id}/task.json).
This module is the single programmatic interface used by the planner, tester and developer
personas to inspect and mutate task metadata.

The JSON schema is defined in `docs/tasks/task_format.py`. We load it dynamically to avoid
packaging requirements while still benefiting from the TypedDict contracts.

Whenever a write is performed an optional `GitManager` instance can be provided so that the
change is staged and committed, keeping repository state consistent.
"""

from pathlib import Path
from typing import List, Optional, Tuple, Any, cast
import json
import importlib.util
import sys
import os

# ---------------------------------------------------------------------------
# Load the canonical schema so we can use the TypedDicts for type-checking.
# ---------------------------------------------------------------------------

_TASK_FORMAT_PATH = Path(__file__).resolve().parent.parent / "docs" / "tasks" / "task_format.py"
_spec = importlib.util.spec_from_file_location("_task_format", _TASK_FORMAT_PATH)
if _spec is None or _spec.loader is None:  # pragma: no cover — fatal mis-configuration.
    raise ImportError(f"Cannot load task_format.py from {_TASK_FORMAT_PATH}")
_task_format = importlib.util.module_from_spec(_spec)  # type: ignore[arg-type]
_spec.loader.exec_module(_task_format)  # type: ignore[union-attr]

# Re-export so that downstream modules can do `from scripts.task_utils import Task, Feature`.
Task = _task_format.Task  # type: ignore[attr-defined]
Feature = _task_format.Feature  # type: ignore[attr-defined]
Status = _task_format.Status  # type: ignore[attr-defined]

# ---------------------------------------------------------------------------
# Git integration (optional)
# ---------------------------------------------------------------------------
try:
    from scripts.git_manager import GitManager  # noqa: F401 – runtime optional
except ModuleNotFoundError:  # pragma: no cover – tests might not need GitManager
    GitManager = None  # type: ignore[assignment]

# ---------------------------------------------------------------------------
# File helpers
# ---------------------------------------------------------------------------

def _task_file_path(task_id: int | str, base_path: str | Path = "tasks") -> Path:
    """Return the absolute path to tasks/{id}/task.json"""
    return Path(base_path).expanduser().resolve() / str(task_id) / "task.json"


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".json.tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    tmp.replace(path)

# ---------------------------------------------------------------------------
# Public API used by agent personas
# ---------------------------------------------------------------------------

__all__ = [
    "Task",
    "Feature",
    "get_task",
    "save_task",
    "update_feature_status",
    "get_pending_features",
    "add_plan",
    "add_feature",
]

# --- Planner tools ----------------------------------------------------------

def get_task(task_id: int | str, base_path: str | Path = "tasks") -> Task | None:
    """Return task data dict or *None* if file is missing."""
    path = _task_file_path(task_id, base_path)
    if not path.exists():
        return None
    return cast(Task, _load_json(path))


def save_task(task_id: int | str, task_data: Task, *, base_path: str | Path = "tasks", git_manager: "GitManager | None" = None) -> None:
    """Over-write the task.json file with *task_data*.

    If *git_manager* is supplied the change is committed on the active branch.
    """
    path = _task_file_path(task_id, base_path)
    _write_json(path, task_data)

    if git_manager is not None:
        git_manager.stage_file(str(path))
        git_manager.commit(f"Update task {task_id}")


def add_plan(task_id: int | str, plan_content: str, *, base_path: str | Path = "tasks", git_manager: "GitManager | None" = None) -> None:
    """Create or replace tasks/{id}/plan.md with *plan_content* and commit the change if requested."""
    plan_path = Path(base_path).expanduser().resolve() / str(task_id) / "plan.md"
    plan_path.parent.mkdir(parents=True, exist_ok=True)
    plan_path.write_text(plan_content, encoding="utf-8")

    if git_manager is not None:
        git_manager.stage_file(str(plan_path))
        git_manager.commit(f"Add/Update plan for task {task_id}")


def get_pending_features(task_data: Task) -> List[Feature]:
    """Return a list of features whose *status* is marked as pending ("-" or "?" according to current spec)."""
    return [f for f in task_data.get("features", []) if f.get("status") in {"-", "?"}]

# --- Tester / Developer shared tools ---------------------------------------

def update_feature_status(
    task_id: int | str,
    feature_id: str,
    new_status: Status,
    *,
    base_path: str | Path = "tasks",
    git_manager: "GitManager | None" = None,
) -> bool:
    """Update *status* of the given feature. Returns *True* if change applied, *False* otherwise."""
    task_data = get_task(task_id, base_path)
    if not task_data:
        return False

    updated = False
    for feat in task_data.get("features", []):
        if feat.get("id") == feature_id:
            if feat.get("status") != new_status:
                feat["status"] = new_status
                updated = True
            break
    if updated:
        save_task(task_id, task_data, base_path=base_path, git_manager=git_manager)
    return updated

# --- Planner extension ------------------------------------------------------

def add_feature(
    task_id: int | str,
    feature: Feature,
    *,
    base_path: str | Path = "tasks",
    git_manager: "GitManager | None" = None,
) -> None:
    """Append a new *feature* (dict compliant with schema) to tasks/{id}/task.json."""
    task_data = get_task(task_id, base_path) or cast(Task, {"id": int(task_id), "status": "-", "title": "", "action": "", "plan": "", "features": []})
    task_data.setdefault("features", []).append(feature)
    save_task(task_id, task_data, base_path=base_path, git_manager=git_manager)
