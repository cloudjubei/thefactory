import os
import sys
import re


def fail(msg: str):
    print(f"FAIL: {msg}")
    sys.exit(1)


def success(msg: str):
    print(f"PASS: {msg}")
    sys.exit(0)


def main():
    spec_path = "docs/SPEC.md"

    # 1) Existence check
    if not os.path.exists(spec_path):
        fail(f"{spec_path} does not exist.")

    with open(spec_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 2) Reference to SPECIFICATION_GUIDE.md near the top
    #    We consider the first 20 non-empty lines as the 'top'.
    lines = [ln.strip() for ln in content.splitlines()]
    top_non_empty = []
    for ln in lines:
        if ln:
            top_non_empty.append(ln)
        if len(top_non_empty) >= 20:
            break
    top_text = "\n".join(top_non_empty)
    if "specification_guide.md" not in top_text.lower():
        fail("docs/SPEC.md does not reference SPECIFICATION_GUIDE.md near the top.")

    # 3) Required sections as headings: WHAT, CORE IDEAS, ACTIONS
    def has_section(name: str) -> bool:
        # Strict heading match (e.g., '# WHAT')
        pat_strict = re.compile(rf"^\s{{0,3}}#{1,6}\s*{re.escape(name)}\s*$", re.IGNORECASE | re.MULTILINE)
        if pat_strict.search(content):
            return True
        # Relaxed: heading line that contains the term in the heading text
        pat_relaxed = re.compile(rf"^\s{{0,3}}#{1,6}\s*.*{re.escape(name)}.*$", re.IGNORECASE | re.MULTILINE)
        return bool(pat_relaxed.search(content))

    required = ["WHAT", "CORE IDEAS", "ACTIONS"]
    missing = [name for name in required if not has_section(name)]
    if missing:
        fail("Missing required section headings: " + ", ".join(missing))

    success("docs/SPEC.md exists, references SPECIFICATION_GUIDE.md at the top, and contains required sections (WHAT, CORE IDEAS, ACTIONS).")


if __name__ == "__main__":
    main()
