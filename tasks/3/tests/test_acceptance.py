import os, sys

def run_test():
    path = "docs/FILE_ORGANISATION.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    content = open(path, "r", encoding="utf-8").read()
    required = [
        "# File Organisation",
        "Top-Level Directory Structure",
        "Directory Descriptions",
        "File Naming Conventions"
    ]
    missing = [s for s in required if s not in content]
    if missing:
        print(f"FAIL: {path} missing: {', '.join(missing)}")
        sys.exit(1)
    print("PASS: Task 3 acceptance verified.")
    sys.exit(0)

if __name__ == "__main__":
    run_test()
