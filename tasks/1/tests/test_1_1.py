import os, sys, re

def run():
    path = "tasks/TASKS.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if "TASK_FORMAT.md" not in content:
        print("FAIL: TASKS.md does not reference TASK_FORMAT.md at the top.")
        sys.exit(1)
    # Verify at least the first task line adheres to the format
    m = re.search(r"^\s*1\)\s[+\-~\?/=]\sTask format", content, re.M)
    if not m:
        print("FAIL: TASKS.md does not adhere to the required task line format for task 1.")
        sys.exit(1)
    print("PASS: TASK 1 acceptance verified: TASKS.md references TASK_FORMAT and adheres to format.")
    sys.exit(0)

if __name__ == "__main__":
    run()
