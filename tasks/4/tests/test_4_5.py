import os, sys

def run():
    path = "docs/SPEC.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    required = [
        "# Problem Statement",
        "# Inputs and Outputs",
        "# Constraints",
        "# Success Criteria",
        "# Edge Cases",
        "# Examples",
    ]

    missing = [h for h in required if h not in content]
    if missing:
        print("FAIL: SPEC.md missing required headings: " + ", ".join(missing))
        sys.exit(1)

    # Verify order of headings is correct
    indices = [content.find(h) for h in required]
    if any(i == -1 for i in indices):
        print("FAIL: Unexpected missing heading when checking order.")
        sys.exit(1)
    if any(indices[i] >= indices[i+1] for i in range(len(indices)-1)):
        print("FAIL: Headings are not in the required order.")
        sys.exit(1)

    print("PASS: SPEC.md contains required headings in correct order.")
    sys.exit(0)

if __name__ == "__main__":
    run()
