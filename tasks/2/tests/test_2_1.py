import os, sys

def run():
    doc = "docs/SPEC.md"
    if not os.path.exists(doc):
        print(f"FAIL: {doc} does not exist.")
        sys.exit(1)
    with open(doc, "r", encoding="utf-8") as f:
        c = f.read()
    if "# WHAT:" not in c:
        print("FAIL: SPEC.md missing '# WHAT:' section header.")
        sys.exit(1)
    print("PASS: SPEC.md exists and contains WHAT section.")
    sys.exit(0)

if __name__ == "__main__":
    run()
