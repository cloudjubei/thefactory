import os, sys

def run():
    required = [
        "tasks/1/tests/test_1_1.py",
        "tasks/2/tests/test_2_1.py",
        "tasks/3/tests/test_3_1.py",
        "tasks/4/tests/test_4_1.py",
        "tasks/5/tests/test_5_1.py",
        "tasks/6/tests/test_6_1.py",
        "tasks/7/tests/test_7_1.py",
        "tasks/8/tests/test_8_1.py",
    ]
    missing = [p for p in required if not os.path.exists(p)]
    if missing:
        print("FAIL: Missing per-task tests: " + ", ".join(missing))
        sys.exit(1)
    print("PASS: Feature 9.2 verified: Per-task tests for Tasks 1–8 exist.")
    sys.exit(0)

if __name__ == "__main__":
    run()
