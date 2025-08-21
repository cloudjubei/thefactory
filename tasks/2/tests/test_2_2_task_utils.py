import json
from pathlib import Path
import importlib

import pytest

# Ensure scripts directory is on sys.path for the test environment
import sys
sys.path.append(str(Path(__file__).resolve().parents[3] / "scripts"))

# Import the module under test
spec = importlib.util.spec_from_file_location("task_utils", str(Path(__file__).resolve().parents[3] / "scripts" / "task_utils.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)  # type: ignore

def test_module_exists_and_has_api():
    required_funcs = [
        "get_task",
        "save_task",
        "update_feature_status",
        "get_pending_features",
        "add_plan",
        "add_feature",
    ]
    for fn in required_funcs:
        assert hasattr(module, fn), f"Expected function '{fn}' in task_utils module"


def test_get_task_returns_correct_id():
    task = module.get_task(2, base_path=Path(__file__).parents[3] / "tasks")
    assert task is not None, "get_task should return data for existing task 2"
    assert task["id"] == 2


def test_update_feature_status_roundtrip(tmp_path):
    """Write a tiny task file to tmp_path and ensure status update persists."""
    # minimal task data with single feature
    task_data = {
        "id": 99,
        "status": "-",
        "title": "dummy",
        "action": "",
        "plan": "",
        "features": [
            {"id": "99.1", "status": "-", "title": "f", "action": "", "plan": "", "context": [], "acceptance": []}
        ],
    }
    base_tasks = tmp_path / "tasks"
    (base_tasks / "99").mkdir(parents=True)
    task_file = base_tasks / "99" / "task.json"
    task_file.write_text(json.dumps(task_data))

    # perform update
    updated = module.update_feature_status(99, "99.1", "+", base_path=base_tasks)
    assert updated, "Status should be updated"

    reloaded = module.get_task(99, base_path=base_tasks)
    assert reloaded["features"][0]["status"] == "+", "Persisted status should be '+'"
