import os, sys

REQUIRED = list(range(1, 11))

def check_plan(task_id):
    path = f"tasks/{task_id}/plan_{task_id}.md"
    if not os.path.exists(path):
        print(f"FAIL: Missing plan file: {path}")
        return False
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if f"# Plan for Task {task_id}:" not in content:
        print(f"FAIL: Plan {path} missing title header.")
        return False
    if "## Features" not in content:
        print(f"FAIL: Plan {path} missing '## Features' section.")
        return False
    return True

def run():
    all_ok = True
    for tid in REQUIRED:
        if not check_plan(tid):
            all_ok = False
    if not all_ok:
        sys.exit(1)
    print("PASS: Plan files for tasks 1–10 exist and contain required sections.")
    sys.exit(0)

if __name__ == "__main__":
    run()
