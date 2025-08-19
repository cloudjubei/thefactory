import os, sys

def run():
    doc = "docs/PLAN_SPECIFICATION.md"
    if not os.path.exists(doc):
        print(f"FAIL: {doc} does not exist.")
        sys.exit(1)
    with open(doc, "r", encoding="utf-8") as f:
        c = f.read()
    phrase = "A feature is not considered complete until a corresponding test is written and passes."
    if phrase not in c:
        print("FAIL: PLAN_SPECIFICATION.md missing exact test-driven acceptance phrase.")
        sys.exit(1)
    print("PASS: PLAN_SPECIFICATION.md encodes test-driven acceptance policy.")
    sys.exit(0)

if __name__ == "__main__":
    run()
