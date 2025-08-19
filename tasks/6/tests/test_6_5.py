import os, sys

def run():
    tasks_md = "tasks/TASKS.md"
    if not os.path.exists(tasks_md):
        print(f"FAIL: {tasks_md} does not exist.")
        sys.exit(1)
    with open(tasks_md, "r", encoding="utf-8") as f:
        content = f.read()

    if "12) = " not in content:
        print("FAIL: Task 12 is not marked as '=' (Deprecated).")
        sys.exit(1)
    if "Deprecated" not in content:
        print("FAIL: Task 12 deprecation note is missing 'Deprecated'.")
        sys.exit(1)
    # Prefer a clear supersession note referencing Task 6
    if "Superseded by Task 6" not in content and "Superseded" not in content:
        print("FAIL: Task 12 does not clearly indicate it is superseded by Task 6.")
        sys.exit(1)

    print("PASS: Task 12 is marked deprecated with explanatory note.")
    sys.exit(0)

if __name__ == "__main__":
    run()
