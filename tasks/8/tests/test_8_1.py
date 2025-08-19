import os
import sys


def run_test():
    path = "docs/TESTING.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if "Agent Testing Specification" not in content:
        print("FAIL: TESTING.md missing title or key phrase.")
        sys.exit(1)
    print("PASS: TESTING.md exists with key phrase.")
    sys.exit(0)


if __name__ == "__main__":
    run_test()
