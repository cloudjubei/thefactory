import os
import sys

def run():
    path = "docs/FILE_ORGANISATION.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    required_sections = [
        "Top-Level Directory Layout",
        "File Naming Conventions",
        "Evolution Guidance"
    ]
    
    missing = []
    for section in required_sections:
        # Check for markdown headers
        if f"# {section}" not in content and f"## {section}" not in content and f"### {section}" not in content:
            missing.append(section)
            
    if missing:
        print(f"FAIL: Missing sections in {path}: {', '.join(missing)}")
        sys.exit(1)

    print(f"PASS: {path} exists and contains all required sections.")
    sys.exit(0)

if __name__ == "__main__":
    run()
