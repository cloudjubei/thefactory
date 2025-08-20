import sys
import os

def run():
    file_path = "docs/FILE_ORGANISATION.md"
    
    # Acceptance Criterion 1: `docs/FILE_ORGANISATION.md` exists
    if not os.path.exists(file_path):
        print(f"FAIL: {file_path} does not exist.")
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Acceptance Criterion 2: It includes clearly titled sections
    required_sections = [
        "Top-Level Directory Layout",
        "File Naming Conventions",
        "Evolution Guidance"
    ]

    missing = [section for section in required_sections if section not in content]

    if missing:
        print(f"FAIL: Missing sections in {file_path}: {', '.join(missing)}")
        sys.exit(1)

    print(f"PASS: {file_path} exists and contains all required sections.")
    sys.exit(0)

if __name__ == "__main__":
    run()
