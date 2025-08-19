import os
import sys

def run():
    path = "docs/PLAN_SPECIFICATION.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    required = [
        "Test-Driven Acceptance",
        "tasks/{task_id}/tests/",
        "scripts/run_tests.py",
        "A feature is not considered complete until a corresponding test is written and passes."
    ]
    missing = [r for r in required if r not in content]
    if missing:
        print("FAIL: PLAN_SPECIFICATION.md missing: " + ", ".join(missing))
        sys.exit(1)
    print("PASS: Task 9.1 - PLAN_SPECIFICATION.md encodes test-driven policy and references test runner/location.")
    sys.exit(0)

if __name__ == "__main__":
    run()
