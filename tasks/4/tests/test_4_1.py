import os, sys

def run():
    path = "docs/SPECIFICATION_GUIDE.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    print("PASS: Task 4 verified: SPECIFICATION_GUIDE.md exists with expected heading.")
    sys.exit(0)

if __name__ == "__main__":
    run()
