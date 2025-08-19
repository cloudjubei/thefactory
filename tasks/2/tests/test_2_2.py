import os, sys

def run():
    path = "docs/TEMPLATE.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    required_headings = [
        "# Problem Statement",
        "# Inputs and Outputs",
        "# Constraints",
        "# Success Criteria",
        "# Edge Cases",
        "# Examples",
    ]

    missing = [h for h in required_headings if h not in content]
    if missing:
        print("FAIL: Missing required headings: " + ", ".join(missing))
        sys.exit(1)

    placeholder_count = content.count("Placeholder:")
    example_count = content.count("Example:")

    if placeholder_count < 6:
        print(f"FAIL: Expected at least 6 'Placeholder:' entries, found {placeholder_count}.")
        sys.exit(1)
    if example_count < 6:
        print(f"FAIL: Expected at least 6 'Example:' entries, found {example_count}.")
        sys.exit(1)

    print("PASS: TEMPLATE.md contains required sections with placeholders and example snippets.")
    sys.exit(0)

if __name__ == "__main__":
    run()
