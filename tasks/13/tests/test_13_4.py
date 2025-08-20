import os
import sys
import json
import runpy


def load_module(path):
    return runpy.run_path(path)


def assert_true(cond, msg):
    if not cond:
        print(f"FAIL: {msg}")
        sys.exit(1)


def read_text(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def main():
    # 1) Verify file exists
    module_path = "scripts/tools/task_utils.py"
    assert_true(os.path.exists(module_path), f"{module_path} does not exist")

    # 2) Check it references the schema types directly
    src = read_text(module_path)
    assert_true("from docs.tasks.task_format import" in src or "import docs.tasks.task_format" in src,
                "task_utils.py should import from docs.tasks.task_format")

    # 3) Load module via runpy and check required functions
    ns = load_module(module_path)
    required = [
        'get_task', 'update_task', 'create_task',
        'update_task_status', 'update_feature_status',
        'ask_agent_question', 'get_feature', 'update_feature'
    ]
    for name in required:
        assert_true(name in ns and callable(ns[name]), f"Missing function: {name}")

    # 4) Exercise core functions using a temporary task id
    base_path = 'tasks'
    temp_id = 13004

    # Create a task with one feature
    create_task = ns['create_task']
    task = create_task(
        temp_id,
        title="Temporary Test Task",
        action="Temp action",
        features=[{
            "id": f"{temp_id}.1",
            "status": "-",
            "title": "Temp Feature",
            "action": "Do something",
            "acceptance": ["Check temp"],
        }],
        status='-',
        plan="",
        acceptance=[{"phase": "P", "criteria": ["C1"]}],
        base_path=base_path,
    )
    task_path = os.path.join(base_path, str(temp_id), 'task.json')
    assert_true(os.path.exists(task_path), f"Expected task file at {task_path}")

    # Load it via get_task
    get_task = ns['get_task']
    loaded = get_task(temp_id, base_path=base_path)
    assert_true(loaded is not None and loaded.get('id') == temp_id, "get_task should return the created task")

    # Update task status
    update_task_status = ns['update_task_status']
    updated = update_task_status(temp_id, '+', base_path=base_path)
    assert_true(updated.get('status') == '+', "Task status should be updated to '+'.")

    # Update feature status
    update_feature_status = ns['update_feature_status']
    updated2 = update_feature_status(temp_id, 1, '~', base_path=base_path)
    feat = updated2['features'][0]
    assert_true(feat.get('status') == '~', "Feature status should be updated to '~'.")

    # Ask agent question at task level
    ask_agent_question = ns['ask_agent_question']
    updated3 = ask_agent_question(temp_id, "Is this a test question?", base_path=base_path)
    assert_true(updated3.get('agent_question') == "Is this a test question?", "Task agent_question was not set correctly.")

    # Ask agent question at feature level
    updated4 = ask_agent_question(temp_id, "Feature Q?", feature_number=1, base_path=base_path)
    feat2 = updated4['features'][0]
    assert_true(feat2.get('agent_question') == "Feature Q?", "Feature agent_question was not set correctly.")

    print("PASS: Feature 13.4 - task_utils tooling implemented and validated.")


if __name__ == '__main__':
    main()
