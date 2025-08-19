import os
import sys

def run():
    path = os.path.join("scripts", "run_tests.py")
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if "tasks" not in content or "tests" not in content:
        print("FAIL: run_tests.py does not appear to discover task tests.")
        sys.exit(1)
    print("PASS: run_tests.py exists and appears to discover tests.")
    sys.exit(0)

if __name__ == "__main__":
    run()
