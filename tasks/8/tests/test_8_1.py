import os, sys

REQUIRED_SECTIONS = [
    "# Agent Testing Specification",
    "## 1) Purpose and Scope",
    "## 2) Test Locations and Naming Conventions",
    "## 3) Test Structure and Utilities",
    "## 4) Writing Acceptance Tests",
    "## 5) Running Tests",
    "## 6) CI/Automation Expectations",
    "## 7) Tool Usage",
    "## 8) Examples",
    "## 9) References",
]


def run():
    path = "docs/TESTING.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"FAIL: Could not read {path}: {e}")
        sys.exit(1)

    missing = [sec for sec in REQUIRED_SECTIONS if sec not in content]
    if missing:
        print("FAIL: Missing required sections in docs/TESTING.md: " + ", ".join(missing))
        sys.exit(1)

    print("PASS: docs/TESTING.md exists and includes all required sections per Task 8.1.")
    sys.exit(0)


if __name__ == "__main__":
    run()
