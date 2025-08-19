import os, sys

def run():
    path = "docs/PLAN_SPECIFICATION.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    checks = [
        ("Testing section header", "## 6. Testing" in content or "\n# Testing" in content or "\n## Testing" in content),
        ("Test file naming guidance", "test_{task_id}_{feature_id}.py" in content),
        ("Tasks tests folder path mention", "tasks/{task_id}/tests/" in content),
        ("finish_feature mention", "finish_feature" in content),
    ]
    missing = [name for name, ok in checks if not ok]
    if missing:
        print("FAIL: PLAN_SPECIFICATION.md missing: " + ", ".join(missing))
        sys.exit(1)
    print("PASS: PLAN_SPECIFICATION.md encodes testing policy and structure.")
    sys.exit(0)

if __name__ == "__main__":
    run()
