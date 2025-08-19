import os
import sys


def fail(msg: str):
    print(f"FAIL: {msg}")
    sys.exit(1)


def run():
    spec_path = "docs/PLAN_SPECIFICATION.md"

    if not os.path.exists(spec_path):
        fail(f"{spec_path} does not exist.")

    with open(spec_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check for the section title
    if "Test-Driven Acceptance" not in content:
        fail("'Test-Driven Acceptance' section not found in PLAN_SPECIFICATION.md")

    # Check for the exact phrase required by acceptance criteria
    phrase = "A feature is not considered complete until a corresponding test is written and passes."
    if phrase not in content:
        fail("Required phrase about feature completion and tests not found in PLAN_SPECIFICATION.md")

    print("PASS: PLAN_SPECIFICATION.md encodes the Test-Driven Acceptance policy and required phrase.")
    sys.exit(0)


if __name__ == "__main__":
    run()
