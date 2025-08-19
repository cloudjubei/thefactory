import os
import sys


def run_test():
    """
    Tests that docs/LOCAL_APP.md was created and contains key sections.
    """
    path = "docs/LOCAL_APP.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    required_sections = [
        "# Local App Project Specification",
        "## References",
        "## Repository Bootstrap",
        "## MVP Success Criteria",
    ]

    missing = [s for s in required_sections if s not in content]
    if missing:
        print(f"FAIL: {path} is missing sections: {', '.join(missing)}")
        sys.exit(1)

    print("PASS: docs/LOCAL_APP.md exists and contains required sections.")
    sys.exit(0)


if __name__ == "__main__":
    run_test()
