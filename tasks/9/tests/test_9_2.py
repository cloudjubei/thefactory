import os
import sys
import glob


def run_test():
    # Ensure that for tasks 1..8 there is at least one test script present
    missing = []
    for tid in range(1, 9):
        pattern = os.path.join("tasks", str(tid), "tests", "*.py")
        files = glob.glob(pattern)
        if not files:
            missing.append(str(tid))
    if missing:
        print("FAIL: Missing test files for tasks: " + ", ".join(missing))
        sys.exit(1)
    print("PASS: Tests exist for tasks 1–8.")
    sys.exit(0)


if __name__ == "__main__":
    run_test()
