import os
import sys


def run_test():
    path = "docs/PLAN_SPECIFICATION.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    required_phrases = [
        "## 6. Testing",  # section header
        "A feature is not considered complete until a corresponding test is written and passes",
        "tasks/{task_id}/tests/",
        "test_{task_id}_{feature_id}.py",
        "scripts/run_tests.py"
    ]

    missing = [p for p in required_phrases if p not in content]
    if missing:
        print("FAIL: PLAN_SPECIFICATION.md missing testing content: " + ", ".join(missing))
        sys.exit(1)

    print("PASS: PLAN_SPECIFICATION.md updated with Testing section and rules.")
    sys.exit(0)


if __name__ == "__main__":
    run_test()
