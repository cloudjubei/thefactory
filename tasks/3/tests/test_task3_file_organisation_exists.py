import os
import sys

def run():
    path = os.path.join("docs", "FILE_ORGANISATION.md")
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if "Top-Level Directory Structure" not in content and "# File Organisation" not in content:
        print("FAIL: FILE_ORGANISATION.md missing expected headings.")
        sys.exit(1)

    print("PASS: FILE_ORGANISATION.md exists with expected headings.")
    sys.exit(0)

if __name__ == "__main__":
    run()
