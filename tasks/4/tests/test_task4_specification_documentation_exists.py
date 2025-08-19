import os
import sys

def run():
    path = os.path.join("docs", "SPECIFICATION_GUIDE.md")
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if "Specification" not in content:
        print("FAIL: SPECIFICATION_GUIDE.md missing expected content.")
        sys.exit(1)

    print("PASS: SPECIFICATION_GUIDE.md exists and contains expected content.")
    sys.exit(0)

if __name__ == "__main__":
    run()
