import os
import sys


def run():
    """
    Tests that docs/TOOL_ARCHITECTURE.md exists and contains key sections for Task 6, Feature 6.5.
    Verifies presence of:
    - "Tool-Using Agent Architecture"
    - "Available Tools"
    - "Mandatory Task Completion Workflow"
    """
    path = "docs/TOOL_ARCHITECTURE.md"

    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)

    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"FAIL: Could not read {path}: {e}")
        sys.exit(1)

    required_phrases = [
        "Tool-Using Agent Architecture",
        "Available Tools",
        "Mandatory Task Completion Workflow",
    ]

    missing = [phrase for phrase in required_phrases if phrase not in content]
    if missing:
        print("FAIL: Missing required sections/phrases: " + ", ".join(missing))
        sys.exit(1)

    print("PASS: TOOL_ARCHITECTURE.md contains all required sections for 6.5.")
    sys.exit(0)


if __name__ == "__main__":
    run()
