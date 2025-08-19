import os, sys

def fail(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)


def run():
    path = "docs/SPEC.md"
    if not os.path.exists(path):
        fail(f"{path} does not exist.")

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines()

    # Check guide reference near the top (first 25 lines)
    top_block = "\n".join(lines[:25])
    if "docs/SPECIFICATION_GUIDE.md" not in top_block:
        fail("docs/SPEC.md does not reference docs/SPECIFICATION_GUIDE.md near the top.")

    # Collect section headings as '## '
    headings = []
    for line in lines:
        if line.startswith("## "):
            headings.append(line[3:].strip())

    required = [
        "Problem Statement",
        "Inputs and Outputs",
        "Constraints",
        "Success Criteria",
        "Edge Cases",
        "Examples",
    ]

    # Ensure all required headings exist and capture their order indices
    indices = []
    for req in required:
        if req not in headings:
            fail(f"Missing required section: {req}")
        indices.append(headings.index(req))

    # Verify order is strictly ascending and starts with Problem Statement
    if indices != sorted(indices):
        fail("Required sections are not in the correct order.")

    if indices[0] != 0:
        fail("An extraneous section appears before 'Problem Statement'.")

    print("PASS: docs/SPEC.md adheres to SPECIFICATION_GUIDE.md structure and ordering.")
    sys.exit(0)


if __name__ == "__main__":
    run()
