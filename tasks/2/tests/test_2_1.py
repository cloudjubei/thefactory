import os
import sys
import re


def run_test():
    """
    Acceptance for Task 2 (Feature 2.1):
      - docs/SPEC.md exists.
      - The document references docs/SPECIFICATION_GUIDE.md at the top.
      - It includes sections: WHAT, CORE IDEAS, ACTIONS.
    """
    spec_path = "docs/SPEC.md"

    # 1) Existence check
    if not os.path.exists(spec_path):
        print(f"FAIL: {spec_path} does not exist.")
        sys.exit(1)

    # 2) Read content
    with open(spec_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    content = "".join(lines)

    # 3) Top reference to SPECIFICATION_GUIDE.md (within first 20 lines)
    top_slice = "".join(lines[:20])
    if "SPECIFICATION_GUIDE.md" not in top_slice:
        print("FAIL: docs/SPEC.md does not reference docs/SPECIFICATION_GUIDE.md at the top (within first 20 lines).")
        sys.exit(1)

    # 4) Required section headers as Markdown headings
    patterns = {
        "WHAT": re.compile(r"^#{1,6}\s*WHAT\b", re.MULTILINE),
        "CORE IDEAS": re.compile(r"^#{1,6}\s*CORE\s+IDEAS\b", re.MULTILINE),
        "ACTIONS": re.compile(r"^#{1,6}\s*ACTIONS\b", re.MULTILINE),
    }
    missing = [name for name, pat in patterns.items() if not pat.search(content)]
    if missing:
        print("FAIL: docs/SPEC.md is missing required section headers: " + ", ".join(missing))
        sys.exit(1)

    print("PASS: docs/SPEC.md exists, references SPECIFICATION_GUIDE.md at the top, and contains required sections WHAT, CORE IDEAS, ACTIONS.")
    sys.exit(0)


if __name__ == "__main__":
    run_test()
