import os
import sys


def run_test():
    """
    Validates Feature 9.1 (Update spec): PLAN_SPECIFICATION has a Testing section
    and specifies location, naming, and per-feature completion behavior.
    Checks:
    - Section header '## 6. Testing'
    - Location pattern 'tasks/{task_id}/tests/'
    - Naming pattern 'test_{task_id}_{feature_id}.py'
    - Mention of 'finish_feature' for per-feature completion
    """
    spec_path = "docs/PLAN_SPECIFICATION.md"
    if not os.path.exists(spec_path):
        print(f"FAIL: {spec_path} does not exist.")
        sys.exit(1)

    with open(spec_path, "r", encoding="utf-8") as f:
        content = f.read()

    checks = {
        "## 6. Testing": "Testing section header missing",
        "tasks/{task_id}/tests/": "Location pattern missing",
        "test_{task_id}_{feature_id}.py": "Naming pattern missing",
        "finish_feature": "finish_feature mention missing",
    }

    missing = [msg for substr, msg in checks.items() if substr not in content]
    if missing:
        print("FAIL: PLAN_SPECIFICATION missing required items: " + ", ".join(missing))
        sys.exit(1)

    print("PASS: PLAN_SPECIFICATION Testing section and details present (Feature 9.1).")
    sys.exit(0)


if __name__ == "__main__":
    run_test()
