import os, sys

def run():
    path = "docs/TESTING.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if "# Agent Testing Specification" not in content and "Testing is a critical part" not in content:
        print("FAIL: TESTING.md missing expected heading or intro.")
        sys.exit(1)
    print("PASS: Task 8 verified: TESTING.md exists with expected content.")
    sys.exit(0)

if __name__ == "__main__":
    run()
