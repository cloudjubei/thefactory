import os
import sys
import json
import shutil
from pathlib import Path

# Add project root to sys.path to allow importing 'scripts.tools.task_utils'
project_root = Path(__file__).resolve().parents[3]
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

try:
    from scripts import task_utils
except ImportError as e:
    print(f"FAIL: Could not import task_utils.py. Error: {e}")
    sys.exit(1)

TEST_TASK_ID = 999
TEST_TASK_ID_MOVED = 9999
TESTS_DIR = Path(__file__).parent
TEMP_TASKS_DIR = TESTS_DIR / "temp_tasks_for_test_1_4"

DUMMY_TASK = {
    "id": TEST_TASK_ID,
    "status": "-",
    "title": "Dummy Task",
    "action": "Dummy Action",
    "plan": "Dummy Plan",
    "features": [
        {
            "id": f"{TEST_TASK_ID}.1",
            "status": "-",
            "title": "Dummy Feature",
            "action": "Dummy feature action",
            "plan": "Dummy feature plan",
            "context": [],
            "acceptance": ["It works."]
        }
    ]
}

def setup():
    if TEMP_TASKS_DIR.exists():
        shutil.rmtree(TEMP_TASKS_DIR)
    TEMP_TASKS_DIR.mkdir()

def cleanup():
    if TEMP_TASKS_DIR.exists():
        shutil.rmtree(TEMP_TASKS_DIR)

def run_test(test_func):
    def wrapper():
        setup()
        try:
            test_func()
        finally:
            cleanup()
    return wrapper

@run_test
def test_create_and_get_task():
    print("Running test_create_and_get_task...")
    created = task_utils.create_task(DUMMY_TASK, base_path=str(TEMP_TASKS_DIR))
    assert created, "create_task should return True for a new task."
    retrieved_task = task_utils.get_task(TEST_TASK_ID, base_path=str(TEMP_TASKS_DIR))
    assert retrieved_task is not None, "get_task should retrieve the created task."
    assert retrieved_task['id'] == TEST_TASK_ID, f"Task ID should be {TEST_TASK_ID}."
    print("...PASSED")

@run_test
def test_update_task():
    print("Running test_update_task...")
    task_utils.create_task(DUMMY_TASK, base_path=str(TEMP_TASKS_DIR))
    task = task_utils.get_task(TEST_TASK_ID, base_path=str(TEMP_TASKS_DIR))
    task['title'] = "Updated Dummy Task"
    updated = task_utils.update_task(task, base_path=str(TEMP_TASKS_DIR))
    assert updated, "update_task should return True."
    retrieved_task = task_utils.get_task(TEST_TASK_ID, base_path=str(TEMP_TASKS_DIR))
    assert retrieved_task['title'] == "Updated Dummy Task", "Task title should be updated."
    print("...PASSED")

@run_test
def test_update_statuses():
    print("Running test_update_statuses...")
    task_utils.create_task(DUMMY_TASK, base_path=str(TEMP_TASKS_DIR))
    task_updated = task_utils.update_task_status(TEST_TASK_ID, '+', base_path=str(TEMP_TASKS_DIR))
    assert task_updated, "update_task_status should return True."
    task = task_utils.get_task(TEST_TASK_ID, base_path=str(TEMP_TASKS_DIR))
    assert task['status'] == '+', "Task status should be updated to '+'+"."
    feature_id = f"{TEST_TASK_ID}.1"
    feature_updated = task_utils.update_feature_status(TEST_TASK_ID, feature_id, '~', base_path=str(TEMP_TASKS_DIR))
    assert feature_updated, "update_feature_status should return True."
    task = task_utils.get_task(TEST_TASK_ID, base_path=str(TEMP_TASKS_DIR))
    assert task['features'][0]['status'] == '~', "Feature status should be updated to '~'."
    print("...PASSED")

@run_test
def test_set_agent_question():
    print("Running test_set_agent_question...")
    task_utils.create_task(DUMMY_TASK, base_path=str(TEMP_TASKS_DIR))
    feature_id = f"{TEST_TASK_ID}.1"
    question = "Is this a test?"
    question_set = task_utils.set_agent_question(TEST_TASK_ID, feature_id, question, base_path=str(TEMP_TASKS_DIR))
    assert question_set, "set_agent_question should return True."
    task = task_utils.get_task(TEST_TASK_ID, base_path=str(TEMP_TASKS_DIR))
    assert task['features'][0]['agent_question'] == question, "agent_question should be set."
    print("...PASSED")

@run_test
def test_move_task():
    print("Running test_move_task...")
    task_utils.create_task(DUMMY_TASK, base_path=str(TEMP_TASKS_DIR))
    moved = task_utils.move_task(TEST_TASK_ID, TEST_TASK_ID_MOVED, base_path=str(TEMP_TASKS_DIR))
    assert moved, "move_task should return True."
    assert not (TEMP_TASKS_DIR / str(TEST_TASK_ID)).exists(), "Old task directory should be gone."
    assert (TEMP_TASKS_DIR / str(TEST_TASK_ID_MOVED)).exists(), "New task directory should exist."
    moved_task = task_utils.get_task(TEST_TASK_ID_MOVED, base_path=str(TEMP_TASKS_DIR))
    assert moved_task is not None, "Should be able to get moved task."
    assert moved_task['id'] == TEST_TASK_ID_MOVED, "Task ID in file should be updated."
    assert moved_task['features'][0]['id'] == f"{TEST_TASK_ID_MOVED}.1", "Feature ID in file should be updated."
    print("...PASSED")

def main():
    try:
        utils_path = project_root / 'scripts' / 'tools' / 'task_utils.py'
        if not utils_path.exists():
             print(f"FAIL: `scripts/tools/task_utils.py` does not exist.")
             sys.exit(1)
        test_create_and_get_task()
        test_update_task()
        test_update_statuses()
        test_set_agent_question()
        test_move_task()
        print("PASS: All tests for task_utils passed.")
        sys.exit(0)
    except AssertionError as e:
        print(f"FAIL: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"FAIL: An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()