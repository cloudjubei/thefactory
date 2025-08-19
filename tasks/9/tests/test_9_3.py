import os
import sys


def run_test():
    """
    Validates Feature 9.3 (test runner exists):
    - scripts/run_tests.py exists
    - It appears runnable (contains an __main__ guard)
    """
    runner_path = "scripts/run_tests.py"
    if not os.path.exists(runner_path):
        print(f"FAIL: {runner_path} does not exist.")
        sys.exit(1)

    with open(runner_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Basic runnable indicator
    if "if __name__ == \"__main__\":" not in content:
        print("FAIL: scripts/run_tests.py does not appear to have a __main__ guard.")
        sys.exit(1)

    print("PASS: scripts/run_tests.py exists and appears runnable (Feature 9.3).")
    sys.exit(0)


if __name__ == "__main__":
    run_test()
