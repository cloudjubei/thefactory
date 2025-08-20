import os
import sys
import json

def run():
    print("Running test for Feature 13.8: Embed Plans in JSON and Finalize Orchestrator")
    errors = []

    # Acceptance Criterion 2: All plan.md files are deleted after migration.
    tasks_dir = 'tasks'
    if os.path.isdir(tasks_dir):
        for entry in os.listdir(tasks_dir):
            task_path = os.path.join(tasks_dir, entry)
            if os.path.isdir(task_path) and entry.isdigit():
                plan_md_path = os.path.join(task_path, 'plan.md')
                if os.path.exists(plan_md_path):
                    errors.append(f"FAIL: Found undeleted plan.md file at {plan_md_path}")

    # Acceptance Criterion 3: run_local_agent.py is simplified to only read the task.json format.
    agent_script_path = 'scripts/run_local_agent.py'
    if not os.path.exists(agent_script_path):
        errors.append(f"FAIL: Orchestrator script not found at {agent_script_path}")
    else:
        with open(agent_script_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'plan.md' in content.lower():
                errors.append(f"FAIL: {agent_script_path} appears to still reference 'plan.md'")

    # Acceptance Criterion 1: Migration script embeds plan.md content into task.json files.
    task_json_path = 'tasks/13/task.json'
    if not os.path.exists(task_json_path):
        errors.append(f"FAIL: Test requires a sample task file at {task_json_path}")
    else:
        with open(task_json_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                if 'plan' not in data:
                    errors.append(f"FAIL: {task_json_path} is missing the required 'plan' field in the root object.")
            except json.JSONDecodeError:
                errors.append(f"FAIL: Could not parse JSON from {task_json_path}")

    if errors:
        for error in errors:
            print(error)
        sys.exit(1)

    print("PASS: Feature 13.8 test checks passed.")
    sys.exit(0)

if __name__ == "__main__":
    run()
