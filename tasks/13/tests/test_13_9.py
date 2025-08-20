import os
import sys
import json
import tempfile
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
try:
    from scripts.tools import task_utils
except ImportError:
    print("FAIL: Could not import task_utils.")
    sys.exit(1)

def run():
    print("--- Running Test for Feature 13.9: Update Docs and Tooling for Plan-in-JSON ---")
    
    # 1. Verify documentation changes
    with open('docs/PLAN_SPECIFICATION.md', 'r') as f:
        content = f.read()
        if '`plan.md`' in content or '`plan` field of the corresponding `tasks/{task_id}/task.json` file' not in content:
            print("FAIL: docs/PLAN_SPECIFICATION.md not updated correctly.")
            sys.exit(1)
    print("PASS: docs/PLAN_SPECIFICATION.md updated.")

    with open('docs/FILE_ORGANISATION.md', 'r') as f:
        content = f.read()
        if 'plan.md' in content:
            print("FAIL: docs/FILE_ORGANISATION.md still references plan.md.")
            sys.exit(1)
    print("PASS: docs/FILE_ORGANISATION.md updated.")

    # 2. Verify tooling changes
    temp_dir = tempfile.mkdtemp()
    try:
        # Setup dummy task
        task_id = 999
        task_data = {
            "id": 999,
            "status": "-",
            "features": [
                {"id": "999.1", "status": "-", "title": "Feature 1"}
            ]
        }
        task_utils.create_task(task_data, base_path=temp_dir)

        # Test update_feature_status
        result = task_utils.update_feature_status(task_id, 1, '+', base_path=temp_dir)
        if not result.get('ok'):
            print(f"FAIL: update_feature_status failed: {result.get('error')}")
            sys.exit(1)
        
        # Verify the change
        updated_task = task_utils.get_task(task_id, base_path=temp_dir)
        if not updated_task or updated_task['features'][0]['status'] != '+':
            print("FAIL: task.json was not updated correctly by update_feature_status.")
            sys.exit(1)
        print("PASS: task_utils.update_feature_status works correctly.")

    finally:
        shutil.rmtree(temp_dir)

    # 3. Verify orchestrator exposure
    with open('scripts/run_local_agent.py', 'r') as f:
        content = f.read()
        if 'def update_feature_status(self' not in content:
            print("FAIL: update_feature_status not found in AgentTools class in run_local_agent.py")
            sys.exit(1)
        if '`update_feature_status(task_id: int, feature_number: int, new_status: str)`' not in content:
             print("FAIL: update_feature_status not listed in system prompt in run_local_agent.py")
             sys.exit(1)

    print("PASS: update_feature_status is exposed as a tool in run_local_agent.py.")

    print("\n--- All tests for feature 13.9 passed! ---")
    sys.exit(0)

if __name__ == "__main__":
    run()
