import os, sys

def run():
    doc = "docs/SPECIFICATION_GUIDE.md"
    if not os.path.exists(doc):
        print(f"FAIL: {doc} does not exist.")
        sys.exit(1)
    with open(doc, "r", encoding="utf-8") as f:
        c = f.read()
    if "# Specification Guide" not in c:
        print("FAIL: SPECIFICATION_GUIDE.md missing title.")
        sys.exit(1)
    print("PASS: SPECIFICATION_GUIDE.md exists with correct title.")
    sys.exit(0)

if __name__ == "__main__":
    run()
