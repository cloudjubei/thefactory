import os
import sys
import re

def extract_heading_texts_upper(content: str):
    headings = set()
    for line in content.splitlines():
        if line.lstrip().startswith('#'):
            text = re.sub(r"^\s*#{1,6}\s*", "", line).strip()
            if text:
                headings.add(text.upper())
    return headings

def run():
    path = "docs/SPEC.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    headings = extract_heading_texts_upper(content)
    required = {"WHAT", "CORE IDEAS", "ACTIONS"}
    missing = [h for h in required if h not in headings]
    if missing:
        print("FAIL: SPEC.md missing required headings: " + ", ".join(missing))
        sys.exit(1)
    top_lines = "\n".join(content.splitlines()[:20])
    if "SPECIFICATION_GUIDE.md" not in top_lines:
        print("FAIL: SPEC.md does not reference 'SPECIFICATION_GUIDE.md' near the top (first 20 lines).")
        sys.exit(1)
    print("PASS: SPEC.md has required structure and references SPECIFICATION_GUIDE.md near the top.")
    sys.exit(0)

if __name__ == "__main__":
    run()
