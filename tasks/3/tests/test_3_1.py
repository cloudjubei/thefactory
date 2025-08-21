import os
import sys

def run():
    path = "docs/CHILD_PROJECTS_SPECIFICATION.md"
    print(f"Checking test for feature 3.1: {path}")

    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        content = f.read().lower()

    required_keywords = ["structure", "projects/", "submodule"]
    missing = [s for s in required_keywords if s not in content]

    if missing:
        print(f"FAIL: Missing keywords in {path}: " + ", ".join(missing))
        sys.exit(1)

    print(f"PASS: {path} exists and contains the required keywords.")
    sys.exit(0)

if __name__ == "__main__":
    run()
