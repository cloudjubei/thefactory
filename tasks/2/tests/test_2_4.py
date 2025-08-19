import os
import sys

def run():
    path = "docs/SPECIFICATION_GUIDE.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    required = [
        "Problem Statement",
        "Inputs and Outputs",
        "Constraints",
        "Success Criteria",
        "Edge Cases",
        "Examples",
    ]
    lower = content.lower()
    missing = [h for h in required if h.lower() not in lower]
    if missing:
        print("FAIL: Missing required sections in SPECIFICATION_GUIDE.md: " + ", ".join(missing))
        sys.exit(1)
    print("PASS: SPECIFICATION_GUIDE.md includes all required sections.")
    sys.exit(0)

if __name__ == "__main__":
    run()
