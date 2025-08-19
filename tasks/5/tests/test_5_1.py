import os, sys

def run():
    doc = "docs/PLAN_SPECIFICATION.md"
    if not os.path.exists(doc):
        print(f"FAIL: {doc} does not exist.")
        sys.exit(1)
    with open(doc, "r", encoding="utf-8") as f:
        c = f.read()
    if "# Plan Specification" not in c or "Feature Completion Protocol" not in c:
        print("FAIL: PLAN_SPECIFICATION.md missing key sections.")
        sys.exit(1)
    print("PASS: PLAN_SPECIFICATION.md exists with key sections.")
    sys.exit(0)

if __name__ == "__main__":
    run()
