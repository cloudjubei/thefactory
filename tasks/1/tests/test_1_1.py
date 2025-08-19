import os, sys

def run():
    doc = "docs/TASK_FORMAT.md"
    if not os.path.exists(doc):
        print(f"FAIL: {doc} does not exist.")
        sys.exit(1)
    tasks = "tasks/TASKS.md"
    if not os.path.exists(tasks):
        print(f"FAIL: {tasks} does not exist.")
        sys.exit(1)
    with open(tasks, "r", encoding="utf-8") as f:
        t = f.read()
    if "TASK_FORMAT.md" not in t:
        print("FAIL: TASKS.md does not reference TASK_FORMAT.md at the top.")
        sys.exit(1)
    print("PASS: Task format doc exists and TASKS.md references it.")
    sys.exit(0)

if __name__ == "__main__":
    run()
