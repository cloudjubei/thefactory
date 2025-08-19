import os
import sys

def run():
    path = "docs/PLAN_SPECIFICATION.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    checks = [
        "# Plan Specification",
        "Test-Driven Acceptance",
        "Use `python scripts/run_tests.py` to discover and run all tests",
        "A feature is not considered complete until a corresponding test is written and passes."
    ]
    missing = [c for c in checks if c not in content]
    if missing:
        print("FAIL: PLAN_SPECIFICATION.md missing required phrases: " + ", ".join(missing))
        sys.exit(1)
    print("PASS: Task 9.4 - PLAN_SPECIFICATION.md documents the test-driven policy and runner usage.")
    sys.exit(0)

if __name__ == "__main__":
    run()
