import os
import sys
import re

def run():
    print("Running test for Feature 13.9: Update Docs and Tooling for Plan-in-JSON")
    errors = []

    # AC 1: `docs/PLAN_SPECIFICATION.md` is updated
    plan_spec_path = 'docs/PLAN_SPECIFICATION.md'
    if not os.path.exists(plan_spec_path):
        errors.append(f"FAIL: {plan_spec_path} not found.")
    else:
        with open(plan_spec_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if '`plan` field' not in content or '`task.json`' not in content:
                errors.append(f"FAIL: {plan_spec_path} does not seem to be updated to describe the `plan` field in `task.json`.")

    # AC 2: `docs/FILE_ORGANISATION.md` is updated
    file_org_path = 'docs/FILE_ORGANISATION.md'
    if os.path.exists(file_org_path):
        with open(file_org_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'plan.md' in content and 'deprecated' not in content.lower():
                 errors.append(f"FAIL: {file_org_path} does not seem to reflect that `plan.md` is deprecated.")

    # AC 3: New function in task_utils.py and exposed in orchestrator
    task_utils_path = 'scripts/tools/task_utils.py'
    if not os.path.exists(task_utils_path):
        errors.append(f"FAIL: {task_utils_path} not found.")
    else:
        with open(task_utils_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if not re.search(r"def\s+update_feature_status\s*\(", content):
                errors.append(f"FAIL: Expected function `update_feature_status` not found in {task_utils_path}.")

    agent_script_path = 'scripts/run_local_agent.py'
    if not os.path.exists(agent_script_path):
        errors.append(f"FAIL: {agent_script_path} not found.")
    else:
        with open(agent_script_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'def update_feature_status' not in content and 'update_feature_status_tool' not in content:
                 errors.append(f"FAIL: `update_feature_status` is not exposed as a tool in {agent_script_path}.")

    if errors:
        for error in errors:
            print(error)
        sys.exit(1)

    print("PASS: Feature 13.9 test checks passed.")
    sys.exit(0)

if __name__ == "__main__":
    run()
