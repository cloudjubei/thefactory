import os, sys


def run():
    tasks_path = "tasks/TASKS.md"
    spec_path = "docs/TASK_FORMAT.md"
    # 1. Files exist
    if not os.path.exists(tasks_path):
        print(f"FAIL: {tasks_path} does not exist.")
        sys.exit(1)
    if not os.path.exists(spec_path):
        print(f"FAIL: {spec_path} does not exist.")
        sys.exit(1)
    # 2. TASKS.md references TASK_FORMAT.md at the top
    with open(tasks_path, "r", encoding="utf-8") as f:
        content = f.read()
    if "TASK_FORMAT.md" not in content or "format reference" not in content:
        print("FAIL: tasks/TASKS.md does not reference TASK_FORMAT.md with the format reference note.")
        sys.exit(1)
    print("PASS: Task 1 verified: TASKS.md references TASK_FORMAT.md and the spec file exists.")
    sys.exit(0)


if __name__ == "__main__":
    run()
