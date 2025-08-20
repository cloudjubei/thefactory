import os
import sys
import json

# Ensure repository root in path for package-style imports
sys.path.insert(0, os.getcwd())

from scripts.tools.task_utils import (
    create_task,
    get_task,
    update_task,
    update_task_status,
    update_feature_status,
    ask_agent_question,
)

def read_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def write_json(path: str, data: dict):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

def run():
    # 1) Verify the utility module exists
    util_path = os.path.join("scripts", "tools", "task_utils.py")
    if not os.path.exists(util_path):
        print(f"FAIL: {util_path} does not exist.")
        sys.exit(1)

    # 2) Create a new test task using the utilities
    test_task_id = 1303003  # unlikely to collide
    base_dir = os.path.join("tasks", str(test_task_id))
    task_json_path = os.path.join(base_dir, "task.json")

    task_data = {
        "id": test_task_id,
        "title": "TEST: Utility Task",
        "status": "-",
        "action": "Test the task utilities for JSON format.",
        "plan": "Test-only task plan.",
        "features": [
            {
                "id": f"{test_task_id}.1",
                "status": "-",
                "title": "Test Feature",
                "action": "Test feature status and question updates.",
                "plan": "Test-only feature plan.",
                "context": [],
                "acceptance": []
            }
        ]
    }

    create_task(task_data)

    # 3) Validate files created
    if not os.path.exists(task_json_path):
        print(f"FAIL: {task_json_path} was not created.")
        sys.exit(1)
    created = read_json(task_json_path)
    if str(created.get("id")) != str(test_task_id):
        print("FAIL: Created task has wrong id.")
        sys.exit(1)

    # 4) get_task should return the same data
    loaded = get_task(test_task_id)
    if str(loaded.get("id")) != str(test_task_id):
        print("FAIL: get_task returned wrong task.")
        sys.exit(1)

    # 5) update_task_status -> '+'
    updated = update_task_status(test_task_id, "+")
    if updated.get("status") != "+":
        print("FAIL: update_task_status did not set '+'.")
        sys.exit(1)

    # 6) update_feature_status -> '~' for feature 1
    feat = update_feature_status(test_task_id, 1, "~")
    if feat.get("status") != "~":
        print("FAIL: update_feature_status did not set '~' on feature 1.")
        sys.exit(1)

    # 7) ask_agent_question on feature
    ask_agent_question(test_task_id, "Is this feature clear?", feature_id=1)
    loaded2 = get_task(test_task_id)
    f0 = None
    for f in loaded2.get("features", []):
        if str(f.get("id", "")).endswith(".1"):
            f0 = f
            break
    if not f0 or f0.get("agent_question") != "Is this feature clear?":
        print("FAIL: Feature agent_question not set correctly.")
        sys.exit(1)

    # 8) ask_agent_question on task level
    ask_agent_question(test_task_id, "Overall question at task level")
    loaded3 = get_task(test_task_id)
    if loaded3.get("agent_question") != "Overall question at task level":
        print("FAIL: Task-level agent_question not set correctly.")
        sys.exit(1)

    # 9) update_task (modify title) and verify persistence
    loaded3["title"] = "TEST: Utility Task (updated)"
    update_task(test_task_id, loaded3)
    loaded4 = get_task(test_task_id)
    if loaded4.get("title") != "TEST: Utility Task (updated)":
        print("FAIL: update_task did not persist changes.")
        sys.exit(1)

    print("PASS: task_utils implements required functions and they work as expected.")
    sys.exit(0)

if __name__ == "__main__":
    run()
