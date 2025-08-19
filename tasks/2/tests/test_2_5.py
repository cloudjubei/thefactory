import os
import sys
import re

def has_md_header(content: str, title: str) -> bool:
    # Matches lines like "# Title" or "## Title" up to ######
    pattern = re.compile(r"(?mi)^\s{0,3}#{1,6}\s+" + re.escape(title) + r"\b")
    return bool(pattern.search(content))

def run():
    path = "docs/TEMPLATE.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    titles = [
        "Problem Statement",
        "Inputs and Outputs",
        "Constraints",
        "Success Criteria",
        "Edge Cases",
        "Examples",
    ]
    missing = [t for t in titles if not has_md_header(content, t)]
    if missing:
        print("FAIL: TEMPLATE.md missing required headers: " + ", ".join(missing))
        sys.exit(1)
    print("PASS: TEMPLATE.md includes all required headers.")
    sys.exit(0)

if __name__ == "__main__":
    run()
