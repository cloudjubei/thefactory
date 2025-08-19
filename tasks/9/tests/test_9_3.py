import os
import sys


def run_test():
    path = "scripts/run_tests.py"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if "if __name__ == \"__main__\":" not in content:
        print("FAIL: run_tests.py missing main guard.")
        sys.exit(1)
    print("PASS: run_tests.py exists.")
    sys.exit(0)


if __name__ == "__main__":
    run_test()
