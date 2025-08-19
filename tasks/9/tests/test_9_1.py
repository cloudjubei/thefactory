import os, sys

def run():
    path = "docs/PLAN_SPECIFICATION.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    checks = [
        "## 6. Testing",
        "tasks/{task_id}/tests/",
        "test_{task_id}_{feature_id}.py",
        "Example:",
        "def run():"
    ]
    missing = [c for c in checks if c not in content]
    if missing:
        print("FAIL: PLAN_SPECIFICATION.md testing section missing: " + ", ".join(missing))
        sys.exit(1)
    print("PASS: Task 9.1 acceptance verified.")
    sys.exit(0)

if __name__ == "__main__":
    run()
