import os, sys

def run():
    doc = "docs/FILE_ORGANISATION.md"
    if not os.path.exists(doc):
        print(f"FAIL: {doc} does not exist.")
        sys.exit(1)
    with open(doc, "r", encoding="utf-8") as f:
        c = f.read()
    if "# File Organisation" not in c:
        print("FAIL: FILE_ORGANISATION.md missing title header.")
        sys.exit(1)
    print("PASS: FILE_ORGANISATION.md exists with proper title.")
    sys.exit(0)

if __name__ == "__main__":
    run()
