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

TARGET_FILES = [
    ("docs/SPECIFICATION_GUIDE.md", "SPECIFICATION_GUIDE.md"),
    ("docs/TEMPLATE.md", "TEMPLATE.md"),
]

def check_file(path: str, label: str) -> list:
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        return [f"{label} missing file"]
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    missing = [h for h in REQUIRED_HEADINGS if h not in content]
    if missing:
        print(f"FAIL: {label} is missing headings: {', '.join(missing)}")
    return missing

def run():
    all_missing = []
    for path, label in TARGET_FILES:
        missing = check_file(path, label)
        if missing:
            all_missing.append((label, missing))
    if all_missing:
        # Provide a concise rejection summary similar to the plan's expectations
        spec_missing = next((m for lbl, m in all_missing if lbl == "SPECIFICATION_GUIDE.md"), [])
        tmpl_missing = next((m for lbl, m in all_missing if lbl == "TEMPLATE.md"), [])
        # Exit with failure
        sys.exit(1)
    print("PASS: SPECIFICATION_GUIDE.md and TEMPLATE.md exist and contain all required headings.")
    sys.exit(0)

if __name__ == "__main__":
    run()
