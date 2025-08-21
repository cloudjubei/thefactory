import os, sys

PATH = "docs/FILE_ORGANISATION.md"


def fail(msg: str):
    print(f"FAIL: {msg}")
    sys.exit(1)


def main():
    if not os.path.exists(PATH):
        fail(f"{PATH} does not exist.")
    with open(PATH, "r", encoding="utf-8") as f:
        content = f.read()

    required_sections = [
        "## Top-Level Directory Layout",
        "## File Naming Conventions",
        "## Evolution Guidance",
        "## Example Tree (illustrative)",
    ]
    missing = [s for s in required_sections if s not in content]
    if missing:
        fail("Missing sections: " + ", ".join(missing))

    # Check the example tree looks graphical (box-drawing characters) and references repo_root
    tree_markers = ["├─", "└─"]
    has_graphical = any(m in content for m in tree_markers)
    if not ("repo_root" in content and has_graphical):
        fail("Example tree is not graphical or missing expected markers (├─/└─) and repo_root.")

    print("PASS: FILE_ORGANISATION.md exists with required sections and an illustrative graphical tree.")
    sys.exit(0)


if __name__ == "__main__":
    main()
