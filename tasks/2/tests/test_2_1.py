import os
import sys


def run_test():
    path = "docs/SPEC.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if "# WHAT:" not in content:
        print("FAIL: SPEC.md missing '# WHAT:' section header.")
        sys.exit(1)
    print("PASS: SPEC.md exists with WHAT section.")
    sys.exit(0)


if __name__ == "__main__":
    run_test()
