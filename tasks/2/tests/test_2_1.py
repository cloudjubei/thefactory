import os
import re
import sys

def run_test():
    spec_path = "docs/SPEC.md"

    # 1) File existence
    if not os.path.exists(spec_path):
        print(f"FAIL: {spec_path} does not exist.")
        sys.exit(1)

    with open(spec_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 2) Required sections as Markdown headers (case-insensitive)
    patterns = [
        (r"^\s*#+\s*WHAT\b", "WHAT"),
        (r"^\s*#+\s*CORE\s+IDEAS\b", "CORE IDEAS"),
        (r"^\s*#+\s*ACTIONS\b", "ACTIONS"),
    ]

    missing = []
    for regex, name in patterns:
        if not re.search(regex, content, flags=re.IGNORECASE | re.MULTILINE):
            missing.append(name)

    if missing:
        print("FAIL: Missing required section headers: " + ", ".join(missing))
        sys.exit(1)

    # 3) Reference to SPECIFICATION_GUIDE.md near the top
    with open(spec_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    nonempty = [ln.strip() for ln in lines if ln.strip()]
    top_window = nonempty[:15] if len(nonempty) >= 15 else nonempty

    if not any("SPECIFICATION_GUIDE.md" in ln for ln in top_window):
        print("FAIL: SPECIFICATION_GUIDE.md reference not found near the top of docs/SPEC.md (within first 15 non-empty lines).")
        sys.exit(1)

    print("PASS: docs/SPEC.md exists, contains WHAT, CORE IDEAS, ACTIONS headers, and references SPECIFICATION_GUIDE.md near the top.")
    sys.exit(0)

if __name__ == "__main__":
    run_test()
