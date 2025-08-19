import os
import sys
import glob


def run():
    missing = []
    for tid in range(1, 9):
        test_dir = os.path.join("tasks", str(tid), "tests")
        files = glob.glob(os.path.join(test_dir, "*.py"))
        if not files:
            missing.append(str(tid))
    if missing:
        print(f"FAIL: No tests found for task(s): {', '.join(missing)}")
        sys.exit(1)
    print("PASS: Tests exist for tasks 1–8.")
    sys.exit(0)


if __name__ == "__main__":
    run()
