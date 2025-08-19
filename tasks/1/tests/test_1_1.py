import os
import sys


def run():
    """
    Tests Task 1, Feature 1.1 (Create Task Format specification).
    Acceptance (encoded):
    - docs/TASK_FORMAT.md exists
    - Contains core sections/terms: Field Definitions, Statuses, Rules, Sequential Knowledge, Non-Redundancy, Examples, Tips
    """
    spec_path = "docs/TASK_FORMAT.md"

    if not os.path.exists(spec_path):
        print(f"FAIL: {spec_path} does not exist.")
        sys.exit(1)

    with open(spec_path, "r", encoding="utf-8") as f:
        content = f.read()

    required_terms = [
        "Field Definitions",
        "Statuses",
        "Rules",
        "Sequential Knowledge",
        "Non-Redundancy",
        "Examples",
        "Tips",
    ]

    missing = [term for term in required_terms if term not in content]
    if missing:
        print(f"FAIL: {spec_path} is missing required terms/sections: {', '.join(missing)}")
        sys.exit(1)

    print("PASS: docs/TASK_FORMAT.md exists and contains required sections and rule names.")
    sys.exit(0)


if __name__ == "__main__":
    run()
