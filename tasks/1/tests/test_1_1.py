import os
import sys


def run_test():
    tf_path = "docs/TASK_FORMAT.md"
    tasks_md = "tasks/TASKS.md"

    if not os.path.exists(tf_path):
        print(f"FAIL: {tf_path} does not exist.")
        sys.exit(1)

    if not os.path.exists(tasks_md):
        print(f"FAIL: {tasks_md} does not exist.")
        sys.exit(1)

    with open(tasks_md, "r", encoding="utf-8") as f:
        tasks_content = f.read()

    if "TASK_FORMAT.md" not in tasks_content:
        print("FAIL: tasks/TASKS.md does not reference TASK_FORMAT.md at the top.")
        sys.exit(1)

    print("PASS: Task format doc exists and is referenced in tasks/TASKS.md.")
    sys.exit(0)


if __name__ == "__main__":
    run_test()
