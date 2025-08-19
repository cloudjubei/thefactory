import os, sys

def run():
    path = "docs/SPEC.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if "# WHAT:" not in content and "Specification Programming" not in content:
        print("FAIL: SPEC.md missing expected headings or key phrases.")
        sys.exit(1)
    print("PASS: Task 2 verified: SPEC.md exists with expected content.")
    sys.exit(0)

if __name__ == "__main__":
    run()
