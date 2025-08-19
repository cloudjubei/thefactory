import os, sys, re

def run():
    tasks_md = "tasks/TASKS.md"
    plan_path = "tasks/6/plan_6.md"

    # Check TASKS.md content
    if not os.path.exists(tasks_md):
        print(f"FAIL: {tasks_md} does not exist.")
        sys.exit(1)
    with open(tasks_md, "r", encoding="utf-8") as f:
        tasks_content = f.read()

    # Ensure Task 7 and Task 10 are not present
    for task_no in (7, 10):
        pattern = re.compile(rf"^\s*{task_no}\)", re.MULTILINE)
        if pattern.search(tasks_content):
            print(f"FAIL: Task {task_no} still present in tasks/TASKS.md.")
            sys.exit(1)

    # Ensure plan_6 references scripts/run_local_agent.py
    if not os.path.exists(plan_path):
        print(f"FAIL: {plan_path} does not exist.")
        sys.exit(1)
    with open(plan_path, "r", encoding="utf-8") as f:
        plan_content = f.read()
    if "scripts/run_local_agent.py" not in plan_content:
        print("FAIL: tasks/6/plan_6.md does not reference scripts/run_local_agent.py.")
        sys.exit(1)

    # Ensure tasks/7 and tasks/10 directories do not exist
    for d in ("tasks/7", "tasks/10"):
        if os.path.exists(d):
            print(f"FAIL: {d} directory still exists; artifacts not cleaned up.")
            sys.exit(1)

    print("PASS: Consolidation complete: TASKS.md cleaned, plan references orchestrator, and tasks/7 and tasks/10 are absent.")
    sys.exit(0)

if __name__ == "__main__":
    run()
