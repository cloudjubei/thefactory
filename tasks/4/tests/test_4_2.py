import os
import sys

def run_test():
    """
    Feature 4.2 Acceptance Tests:
    - docs/PLAN_SPECIFICATION.md exists
    - Includes sections: Purpose, Core Principles, Location and Structure, Template, Example
    - References docs/FEATURE_FORMAT.md
    """
    target = "docs/PLAN_SPECIFICATION.md"
    if not os.path.exists(target):
        print(f"FAIL: {target} does not exist.")
        sys.exit(1)

    with open(target, "r", encoding="utf-8") as f:
        content = f.read()

    required_sections = [
        "Purpose",
        "Core Principles",
        "Location and Structure",
        "Template",
        "Example",
    ]

    missing_sections = [s for s in required_sections if s not in content]
    if missing_sections:
        print("FAIL: PLAN_SPECIFICATION.md is missing sections: " + ", ".join(missing_sections))
        sys.exit(1)

    if "docs/FEATURE_FORMAT.md" not in content:
        print("FAIL: PLAN_SPECIFICATION.md does not reference docs/FEATURE_FORMAT.md.")
        sys.exit(1)

    print("PASS: docs/PLAN_SPECIFICATION.md includes required sections and references FEATURE_FORMAT.")
    sys.exit(0)

if __name__ == "__main__":
    run_test()
