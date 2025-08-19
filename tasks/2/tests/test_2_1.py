import os, sys

def run():
    path = "docs/SPEC.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if "# WHAT:" not in content and "# What:" not in content:
        print("FAIL: SPEC.md missing WHAT section header.")
        sys.exit(1)
    print("PASS: Task 2 acceptance verified.")
    sys.exit(0)

if __name__ == "__main__":
    run()
