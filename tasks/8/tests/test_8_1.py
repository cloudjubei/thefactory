import os, sys

def run():
    doc = "docs/TESTING.md"
    if not os.path.exists(doc):
        print(f"FAIL: {doc} does not exist.")
        sys.exit(1)
    with open(doc, "r", encoding="utf-8") as f:
        c = f.read()
    if "# Agent Testing Specification" not in c:
        print("FAIL: TESTING.md missing title.")
        sys.exit(1)
    print("PASS: TESTING.md exists with expected title.")
    sys.exit(0)

if __name__ == "__main__":
    run()
