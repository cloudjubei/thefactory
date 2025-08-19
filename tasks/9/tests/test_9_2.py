import os, sys

def run():
    missing = []
    for i in range(1, 9):
        path = f"tasks/{i}/tests/test_{i}_1.py"
        if not os.path.exists(path):
            missing.append(path)
    if missing:
        print("FAIL: Missing per-task tests: " + ", ".join(missing))
        sys.exit(1)
    print("PASS: Tests for tasks 1–8 exist.")
    sys.exit(0)

if __name__ == "__main__":
    run()
