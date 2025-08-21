import os
import sys
import re

PATH = "docs/FILE_ORGANISATION.md"

REQUIRED_HEADINGS = [
    "# Top-Level Directory Layout",
    "# File Naming Conventions",
    "# Evolution Guidance",
    "# Example tree (illustrative)",
]

def section_exists_and_has_content(content: str, heading: str):
    # Find exact heading line
    m = re.search(rf"^\s*{re.escape(heading)}\s*$", content, re.MULTILINE)
    if not m:
        return False, f"Missing heading: {heading}"
    start = m.end()
    # Find the next heading to delimit the section
    next_h = re.search(r"^\s*#\s", content[start:], re.MULTILINE)
    section_text = content[start:] if not next_h else content[start:start + next_h.start()]
    # Check there is at least one non-empty, non-heading line
    lines = [ln.strip() for ln in section_text.splitlines()]
    has_content = any(ln and not ln.startswith('#') for ln in lines)
    if not has_content:
        return False, f"No content under heading: {heading}"
    return True, ""


def run():
    if not os.path.exists(PATH):
        print(f"FAIL: {PATH} does not exist.")
        sys.exit(1)
    with open(PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Check headings and that each section has some content
    for heading in REQUIRED_HEADINGS:
        ok, msg = section_exists_and_has_content(content, heading)
        if not ok:
            print(f"FAIL: {msg}")
            sys.exit(1)

    # Check for a graphical tree in the example (look for common tree glyphs)
    if "├──" not in content and "└──" not in content:
        print("FAIL: Example tree is not graphical (expected tree glyphs like '├──' or '└──').")
        sys.exit(1)

    print("PASS: FILE_ORGANISATION.md exists with required sections and a graphical example tree.")
    sys.exit(0)


if __name__ == "__main__":
    run()
