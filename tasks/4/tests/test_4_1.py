import os
import sys

def run():
    path = "docs/SPECIFICATION_GUIDE.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if "# Specification Guide" not in content:
        print("FAIL: SPECIFICATION_GUIDE.md is missing '# Specification Guide'.")
        sys.exit(1)
    print("PASS: Task 4 - SPECIFICATION_GUIDE.md exists with expected heading.")
    sys.exit(0)

if __name__ == "__main__":
    run()
