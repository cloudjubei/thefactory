import os
import sys

def run_test():
    """
    Tests for Feature 1.5: File Organisation specification.
    - Verifies that docs/FILE_ORGANISATION.md exists.
    - Verifies that it contains the required sections.
    """
    file_path = "docs/FILE_ORGANISATION.md"
    
    # 1. Check if file exists
    if not os.path.exists(file_path):
        print(f"FAIL: {file_path} does not exist.")
        sys.exit(1)

    # 2. Check for required sections
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"FAIL: Could not read {file_path}: {e}")
        sys.exit(1)

    required_headings = [
        "# Top-Level Directory Layout",
        "# File Naming Conventions",
        "# Evolution Guidance",
        "# Example Tree"
    ]
    
    missing_headings = []
    for heading in required_headings:
        if heading not in content:
            missing_headings.append(heading)

    if missing_headings:
        print(f"FAIL: Missing sections in {file_path}: {', '.join(missing_headings)}")
        sys.exit(1)
        
    print("PASS: docs/FILE_ORGANISATION.md exists and contains all required sections.")
    sys.exit(0)

if __name__ == "__main__":
    run_test()
