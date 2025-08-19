import os
import sys


def run_test():
    path = "docs/PLAN_SPECIFICATION.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if "# Plan Specification" not in content:
        print("FAIL: PLAN_SPECIFICATION.md missing title header.")
        sys.exit(1)
    print("PASS: PLAN_SPECIFICATION.md exists with title.")
    sys.exit(0)


if __name__ == "__main__":
    run_test()
