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


def assert_exists(path: str):
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)


def check_headings_presence_and_order(content: str, headings: list[str]) -> tuple[list[str], bool]:
    missing = [h for h in headings if h not in content]
    if missing:
        return missing, False
    positions = [content.find(h) for h in headings]
    in_order = positions == sorted(positions)
    return [], in_order


def run_test():
    spec_path = "docs/SPEC.md"
    assert_exists(spec_path)

    with open(spec_path, "r", encoding="utf-8") as f:
        content = f.read()

    missing, in_order = check_headings_presence_and_order(content, REQUIRED_HEADINGS)

    if missing:
        print("FAIL: docs/SPEC.md is missing headings: " + ", ".join(missing))
        sys.exit(1)

    if not in_order:
        print("FAIL: docs/SPEC.md headings are not in the required order.")
        sys.exit(1)

    print("PASS: SPEC.md exists and includes all required headings in the correct order.")
    sys.exit(0)


if __name__ == "__main__":
    run_test()
