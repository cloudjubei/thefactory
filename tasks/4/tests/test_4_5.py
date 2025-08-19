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

def run():
    spec_path = "docs/SPEC.md"
    if not os.path.exists(spec_path):
        print(f"FAIL: {spec_path} does not exist.")
        sys.exit(1)
    with open(spec_path, "r", encoding="utf-8") as f:
        content = f.read()
    missing = [h for h in REQUIRED_HEADINGS if h not in content]
    if missing:
        print(f"FAIL: {spec_path} is missing headings: {', '.join(missing)}")
        sys.exit(1)
    print("PASS: test_4_5 - SPEC.md contains all required headings.")
    sys.exit(0)

if __name__ == "__main__":
    run()
