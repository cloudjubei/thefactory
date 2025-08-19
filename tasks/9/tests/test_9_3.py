import os
import sys

def run():
    path = "scripts/run_tests.py"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if "def main()" not in content or "if __name__ == \"__main__\":" not in content:
        print("FAIL: run_tests.py missing a main entrypoint.")
        sys.exit(1)
    print("PASS: Task 9.3 - run_tests.py exists and has a main entrypoint.")
    sys.exit(0)

if __name__ == "__main__":
    run()
