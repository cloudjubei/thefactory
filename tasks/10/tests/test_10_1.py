import os
import sys


def read(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def run():
    tasks_md = 'tasks/TASKS.md'
    plan6 = 'tasks/6/plan_6.md'

    # Existence checks
    if not os.path.exists(tasks_md):
        print(f"FAIL: {tasks_md} does not exist.")
        sys.exit(1)
    if not os.path.exists(plan6):
        print(f"FAIL: {plan6} does not exist.")
        sys.exit(1)

    content = read(tasks_md)

    # 1) Task 7 (Agent Orchestrator) should no longer be listed
    if 'Agent Orchestrator' in content:
        print("FAIL: Found 'Agent Orchestrator' in TASKS.md; merge not applied.")
        sys.exit(1)

    # 2) Task 6 should reflect the merged title
    expected_title_line = '6) + Agent: Principles and Orchestrator'
    if expected_title_line not in content:
        print(f"FAIL: Expected merged task title line not found: {expected_title_line}")
        sys.exit(1)

    # 3) The merged plan for Task 6 should contain the two completed features
    plan6_content = read(plan6)
    required_snippets = [
        '6.1) + Define Core Agent Terminology and Principles',
        '6.2) + Implement the Agent Orchestrator script'
    ]
    missing = [s for s in required_snippets if s not in plan6_content]
    if missing:
        print('FAIL: tasks/6/plan_6.md is missing: ' + ', '.join(missing))
        sys.exit(1)

    print('PASS: Task 10 merge validated: Task 7 removed, Task 6 merged, and plan updated.')
    sys.exit(0)


if __name__ == '__main__':
    run()
