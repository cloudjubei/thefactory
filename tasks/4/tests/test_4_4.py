import os
import sys

REQUIRED_HEADINGS = [
    "# Problem Statement",
    "# Inputs and Outputs",
    "# Constraints",
    "# Success Criteria",
    "# Edge Cases",
    "# Examples",
]

FILES = [
    ("docs/SPECIFICATION_GUIDE.md", "Specification Guide"),
    ("docs/TEMPLATE.md", "Specification Template"),
]

def check_file(path, label):
    if not os.path.exists(path):
        print(f"FAIL: {label} missing: {path} does not exist.")
        return False
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    missing = [h for h in REQUIRED_HEADINGS if h not in content]
    if missing:
        print(f"FAIL: {label} ({path}) is missing headings: {', '.join(missing)}")
        return False
    print(f"PASS: {label} ({path}) contains all required headings.")
    return True

def run():
    ok = True
    for path, label in FILES:
        ok = check_file(path, label) and ok
    if not ok:
        sys.exit(1)
    print("PASS: test_4_4 - Guide and Template verified.")
    sys.exit(0)

if __name__ == "__main__":
    run()
