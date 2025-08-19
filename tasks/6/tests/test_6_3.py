import os, sys, re

def fail(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)

def pass_msg(msg):
    print(f"PASS: {msg}")
    sys.exit(0)

def run():
    # 1) tasks/TASKS.md no longer includes Task 7 in the current tasks list (no line starting with '7) ')
    tasks_md = "tasks/TASKS.md"
    if not os.path.exists(tasks_md):
        fail(f"{tasks_md} does not exist.")
    with open(tasks_md, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    has_task_7_line = any(re.match(r"^\s*7\)\s", line) for line in lines)
    if has_task_7_line:
        fail("tasks/TASKS.md still lists Task 7 as a current task.")

    # 2) This plan references scripts/run_local_agent.py
    plan_path = "tasks/6/plan_6.md"
    if not os.path.exists(plan_path):
        fail(f"{plan_path} does not exist.")
    with open(plan_path, "r", encoding="utf-8") as f:
        plan_content = f.read()
    if "scripts/run_local_agent.py" not in plan_content:
        fail("tasks/6/plan_6.md does not reference scripts/run_local_agent.py as required.")

    # 3) No tasks/7 artifacts remain (directory should not exist)
    if os.path.exists("tasks/7"):
        fail("Directory tasks/7 still exists; expected it to be removed or merged.")

    pass_msg("Feature 6.3 acceptance criteria satisfied: Task 7 not listed, plan references run_local_agent.py, and no tasks/7 artifacts.")

if __name__ == "__main__":
    run()
