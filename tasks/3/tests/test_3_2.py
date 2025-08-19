#!/usr/bin/env python3
import os
import sys


def run_test():
    """
    Validates Task 3 Feature 3.1 specification file exists and contains required headings.
    Acceptance:
    - docs/FILE_ORGANISATION.md exists
    - Contains: "Top-Level Directory Layout", "File Naming Conventions", "Evolution Guidance"
    """
    target = "docs/FILE_ORGANISATION.md"

    if not os.path.exists(target):
        print(f"FAIL: {target} does not exist.")
        sys.exit(1)

    try:
        with open(target, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"FAIL: Could not read {target}: {e}")
        sys.exit(1)

    required_headings = [
        "Top-Level Directory Layout",
        "File Naming Conventions",
        "Evolution Guidance",
    ]

    missing = [h for h in required_headings if h not in content]
    if missing:
        print("FAIL: Missing required headings: " + ", ".join(missing))
        sys.exit(1)

    print("PASS: docs/FILE_ORGANISATION.md exists and contains required section headings.")
    sys.exit(0)


if __name__ == "__main__":
    run_test()
