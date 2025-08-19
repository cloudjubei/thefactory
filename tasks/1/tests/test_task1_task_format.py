import os
import sys

def run():
    tf_path = os.path.join("docs", "TASK_FORMAT.md")
    tasks_path = os.path.join("tasks", "TASKS.md")

    if not os.path.exists(tf_path):
        print(f"FAIL: {tf_path} does not exist.")
        sys.exit(1)

    if not os.path.exists(tasks_path):
        print(f"FAIL: {tasks_path} does not exist.")
        sys.exit(1)

    with open(tasks_path, "r", encoding="utf-8") as f:
        tasks_content = f.read()

    if "TASK_FORMAT.md" not in tasks_content:
        print("FAIL: tasks/TASKS.md does not reference TASK_FORMAT.md at the top.")
        sys.exit(1)

    print("PASS: Task format doc exists and TASKS.md references it.")
    sys.exit(0)

if __name__ == "__main__":
    run()
