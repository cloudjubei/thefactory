import os
import sys

def run():
    task_format = "docs/TASK_FORMAT.md"
    tasks_md = "tasks/TASKS.md"

    if not os.path.exists(task_format):
        print(f"FAIL: {task_format} does not exist.")
        sys.exit(1)

    if not os.path.exists(tasks_md):
        print(f"FAIL: {tasks_md} does not exist.")
        sys.exit(1)

    with open(tasks_md, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    top = "\n".join(lines[:10])
    if "TASK_FORMAT.md" not in top:
        print("FAIL: TASKS.md does not reference TASK_FORMAT.md near the top.")
        sys.exit(1)

    print("PASS: Task 1 - TASK_FORMAT.md exists and TASKS.md references it at the top.")
    sys.exit(0)

if __name__ == "__main__":
    run()
