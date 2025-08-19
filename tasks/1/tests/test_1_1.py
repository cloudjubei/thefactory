import os
import sys

def run():
    path = "docs/TASK_FORMAT.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    required_sections = [
        "Field Definitions",
        "Statuses",
        "Rules",
        "Examples",
        "Tips",
    ]
    missing = [s for s in required_sections if s not in content]
    if missing:
        print("FAIL: Missing sections: " + ", ".join(missing))
        sys.exit(1)
    print("PASS: TASK_FORMAT.md exists and contains required sections.")
    sys.exit(0)

if __name__ == "__main__":
    run()
