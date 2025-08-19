import os
import sys


def run_test():
    path = "docs/PLAN_SPECIFICATION.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if "A feature is not considered complete until a corresponding test is written and passes" not in content:
        print("FAIL: PLAN_SPECIFICATION.md missing test-driven acceptance policy phrase.")
        sys.exit(1)

    if "scripts/run_tests.py" not in content:
        print("FAIL: PLAN_SPECIFICATION.md missing reference to scripts/run_tests.py")
        sys.exit(1)

    print("PASS: PLAN_SPECIFICATION.md encodes the test-driven acceptance policy and references test runner.")
    sys.exit(0)


if __name__ == "__main__":
    run_test()
