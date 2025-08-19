import os
import sys

def run():
    path = os.path.join("docs", "PLAN_SPECIFICATION.md")
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if "Plan Specification" not in content:
        print("FAIL: PLAN_SPECIFICATION.md missing expected heading.")
        sys.exit(1)

    print("PASS: PLAN_SPECIFICATION.md exists with expected heading.")
    sys.exit(0)

if __name__ == "__main__":
    run()
