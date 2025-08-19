import os
import sys

def run():
    path = "docs/FILE_ORGANISATION.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if "File Organisation" not in content:
        print("FAIL: FILE_ORGANISATION.md does not contain 'File Organisation'.")
        sys.exit(1)
    print("PASS: Task 3 - FILE_ORGANISATION.md exists and contains expected heading.")
    sys.exit(0)

if __name__ == "__main__":
    run()
