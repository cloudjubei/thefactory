import os
import sys
import json
import shutil


def fail(msg: str):
    print(f"FAIL: {msg}")
    sys.exit(1)


def ok(msg: str):
    print(f"PASS: {msg}")
    sys.exit(0)


def main():
    try:
        from scripts.tools import task_utils
    except Exception as e:
        fail(f"Could not import scripts.tools.task_utils: {e}")

    # Verify it exposes canonical types from docs/tasks/task_format.py (direct reference)
    if not all(hasattr(task_utils, name) for name in ("Task", "Feature", "Status")):
        fail("task_utils does not expose Task/Feature/Status types")

    # Verify required functions exist
    required_funcs = [
        "get_task",
        "update_task",
        "create_task",
        "update_task_status",
        "update_feature_status",
        "ask_agent_question",
    ]
    for fn in required_funcs:
        if not hasattr(task_utils, fn):
            fail(f"Missing function: {fn}")

    # Use a temporary base path under this task's tests directory to avoid polluting repo
    base = os.path.join("tasks", "13", "tests", "tmp_tasks")
    if os.path.exists(base):
        shutil.rmtree(base)
    os.makedirs(base, exist_ok=True)

    try:
        task_id = 13003
        sample_task = {
            "id": str(task_id),
            "status": "-",
            "title": "Temporary Task for task_utils tests",
            "action": "Exercise task utility functions.",
            "plan": "Test-only plan.",
            "features": [
                {
                    "id": f"{task_id}.1",
                    "status": "-",
                    "title": "Feature 1",
                    "action": "Do something",
                    "plan": "",
                    "context": [],
                    "acceptance": ["dummy"]
                }
            ]
        }

        # Create task
        try:
            task_utils.create_task(sample_task, base_path=base)
        except Exception as e:
            fail(f"create_task raised an exception: {e}")

        task_json_path = os.path.join(base, str(task_id), "task.json")
        if not os.path.exists(task_json_path):
            fail("create_task did not create the task.json at expected path")

        # get_task
        t = task_utils.get_task(task_id, base_path=base)
        if str(t.get("id")) != str(task_id):
            fail("get_task returned wrong id")

        # update_task_status
        t2 = task_utils.update_task_status(task_id, "+", base_path=base)
        if t2.get("status") != "+":
            fail("update_task_status did not persist '+'.")

        # update_feature_status
        f1 = task_utils.update_feature_status(task_id, 1, "~", base_path=base)
        if f1.get("status") != "~":
            fail("update_feature_status did not set feature status '~'.")

        # ask_agent_question at task level
        t3 = task_utils.ask_agent_question(task_id, None, "Task-level question?", base_path=base)
        if t3.get("agent_question") != "Task-level question?":
            fail("ask_agent_question (task-level) did not set agent_question correctly.")

        # ask_agent_question at feature level
        t4 = task_utils.ask_agent_question(task_id, 1, "Feature-level question?", base_path=base)
        feats = t4.get("features", [])
        feat = next((f for f in feats if f.get("id") == f"{task_id}.1"), None)
        if not feat or feat.get("agent_question") != "Feature-level question?":
            fail("ask_agent_question (feature-level) did not set feature agent_question correctly.")

        # update_task (e.g., change title)
        t4["title"] = "Updated Title"
        t5 = task_utils.update_task(task_id, t4, base_path=base)
        if t5.get("title") != "Updated Title":
            fail("update_task did not persist updated title.")

    finally:
        # Cleanup temporary directory
        if os.path.exists(base):
            shutil.rmtree(base)

    ok("task_utils provides required functions and behavior.")


if __name__ == "__main__":
    main()
