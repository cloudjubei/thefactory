import os
import sys


def run_test():
    """
    Tests that PLAN_SPECIFICATION encodes the test-driven policy for Feature 9.4.
    - Checks docs/PLAN_SPECIFICATION.md exists.
    - Checks for the section title/heading phrase "Test-Driven Acceptance".
    - Checks for the exact phrase: "A feature is not considered complete until a corresponding test is written and passes."
    """
    spec_path = "docs/PLAN_SPECIFICATION.md"
    if not os.path.exists(spec_path):
        print(f"FAIL: {spec_path} does not exist.")
        sys.exit(1)

    with open(spec_path, "r", encoding="utf-8") as f:
        content = f.read()

    required_phrases = [
        "Test-Driven Acceptance",
        "A feature is not considered complete until a corresponding test is written and passes.",
    ]

    missing = [p for p in required_phrases if p not in content]
    if missing:
        print("FAIL: PLAN_SPECIFICATION is missing: " + ", ".join(missing))
        sys.exit(1)

    print("PASS: PLAN_SPECIFICATION encodes the test-driven policy (Feature 9.4).")
    sys.exit(0)


if __name__ == "__main__":
    run_test()
