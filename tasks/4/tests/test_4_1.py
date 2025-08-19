import os, sys

def run():
    path = "docs/SPECIFICATION_GUIDE.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if "# Specification Guide" not in content:
        print("FAIL: SPECIFICATION_GUIDE.md missing expected header.")
        sys.exit(1)
    print("PASS: Task 4 acceptance verified: SPECIFICATION_GUIDE.md exists.")
    sys.exit(0)

if __name__ == "__main__":
    run()
