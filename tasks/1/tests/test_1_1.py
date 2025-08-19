import os, sys

def run():
    ok = True
    # Check Task format doc exists
    path = "docs/TASK_FORMAT.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    # Check TASKS.md references TASK_FORMAT at the top
    tasks_path = "tasks/TASKS.md"
    if not os.path.exists(tasks_path):
        print(f"FAIL: {tasks_path} does not exist.")
        sys.exit(1)
    with open(tasks_path, "r", encoding="utf-8") as f:
        content = f.read()
    if "TASK_FORMAT.md" not in content:
        print("FAIL: tasks/TASKS.md does not reference TASK_FORMAT.md.")
        sys.exit(1)
    print("PASS: Task 1 acceptance verified.")
    sys.exit(0)

if __name__ == "__main__":
    run()
