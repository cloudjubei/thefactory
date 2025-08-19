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


def missing_headings(content: str, required: list[str]) -> list[str]:
    return [h for h in required if h not in content]


def run_test():
    guide_path = "docs/SPECIFICATION_GUIDE.md"
    template_path = "docs/TEMPLATE.md"

    # 1) Existence checks
    assert_exists(guide_path)
    assert_exists(template_path)

    # 2) Heading checks
    with open(guide_path, "r", encoding="utf-8") as f:
        guide_content = f.read()
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    guide_missing = missing_headings(guide_content, REQUIRED_HEADINGS)
    template_missing = missing_headings(template_content, REQUIRED_HEADINGS)

    if guide_missing or template_missing:
        # Provide a deterministic combined rejection message
        g = ", ".join(guide_missing) if guide_missing else "none"
        t = ", ".join(template_missing) if template_missing else "none"
        print(
            "FAIL: Missing required headings. "
            f"docs/SPECIFICATION_GUIDE.md missing: {g} | "
            f"docs/TEMPLATE.md missing: {t}"
        )
        sys.exit(1)

    print("PASS: SPECIFICATION_GUIDE.md and TEMPLATE.md exist and contain all required headings.")
    sys.exit(0)


if __name__ == "__main__":
    run_test()
