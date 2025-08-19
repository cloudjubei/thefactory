import os, sys

def run():
    path = "docs/PLAN_SPECIFICATION.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if "# Plan Specification" not in content:
        print("FAIL: PLAN_SPECIFICATION.md missing main heading.")
        sys.exit(1)
    if "Feature Completion Protocol" not in content and "finish_feature(" not in content:
        print("FAIL: PLAN_SPECIFICATION.md missing feature completion policy details.")
        sys.exit(1)
    print("PASS: Task 5 verified: PLAN_SPECIFICATION.md exists with completion policy references.")
    sys.exit(0)

if __name__ == "__main__":
    run()
