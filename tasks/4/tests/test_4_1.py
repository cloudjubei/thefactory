import os
import sys

def run_test():
    """
    Feature 4.1 Acceptance Tests:
    - docs/FEATURE_FORMAT.md exists
    - Contains sections: Purpose, Where Features Live, Format, Field Definitions, Examples
    - References project specs: docs/TASK_FORMAT.md and docs/SPECIFICATION_GUIDE.md
    """
    target = "docs/FEATURE_FORMAT.md"
    if not os.path.exists(target):
        print(f"FAIL: {target} does not exist.")
        sys.exit(1)

    with open(target, "r", encoding="utf-8") as f:
        content = f.read()

    required_sections = [
        "Purpose",
        "Where Features Live",
        "Format",
        "Field Definitions",
        "Examples",
    ]

    missing_sections = [s for s in required_sections if s not in content]
    if missing_sections:
        print("FAIL: FEATURE_FORMAT.md is missing sections: " + ", ".join(missing_sections))
        sys.exit(1)

    required_refs = [
        "docs/TASK_FORMAT.md",
        "docs/SPECIFICATION_GUIDE.md",
    ]
    missing_refs = [r for r in required_refs if r not in content]
    if missing_refs:
        print("FAIL: FEATURE_FORMAT.md missing references: " + ", ".join(missing_refs))
        sys.exit(1)

    print("PASS: docs/FEATURE_FORMAT.md exists with required sections and references.")
    sys.exit(0)

if __name__ == "__main__":
    run_test()
