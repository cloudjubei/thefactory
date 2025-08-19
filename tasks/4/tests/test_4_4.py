import os, sys, re


def fail(msg: str):
    print(f"FAIL: {msg}")
    sys.exit(1)


def run():
    path = "docs/SPECIFICATION_GUIDE.md"
    if not os.path.exists(path):
        fail(f"{path} does not exist.")

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Required headings per acceptance criteria
    required_headings = [
        "Problem Statement",
        "Inputs and Outputs",
        "Constraints",
        "Success Criteria",
        "Edge Cases",
        "Examples",
    ]

    missing = []
    for heading in required_headings:
        # Match Markdown headings like #, ##, ..., ###### followed by the exact section title
        pattern = re.compile(rf"(?m)^\s*#{{1,6}}\s+{re.escape(heading)}(\s|$)")
        if not pattern.search(content):
            missing.append(heading)

    if missing:
        fail("Missing headings: " + ", ".join(missing))

    print("PASS: SPECIFICATION_GUIDE.md has required headings.")
    sys.exit(0)


if __name__ == "__main__":
    run()
