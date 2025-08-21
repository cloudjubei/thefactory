import os, sys


def run():
    path = "docs/CHILD_PROJECTS_SPECIFICATION.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    lc = content.lower()

    missing = []
    # Title/primary heading
    if "child projects specification" not in lc:
        missing.append("'Child Projects Specification' heading")
    # Must explain projects/ directory
    if "projects/" not in content:
        missing.append("mention of 'projects/' directory")
    # Must explain Git submodules
    if "git submodule" not in lc:
        missing.append("mention of Git submodules")
    # Must detail expected structure with these files
    for required in ["README.md", ".gitignore", "spec.md"]:
        if required not in content:
            missing.append(required)

    if missing:
        print("FAIL: Missing required content: " + ", ".join(missing))
        sys.exit(1)

    print("PASS: CHILD_PROJECTS_SPECIFICATION.md exists and includes structure, projects/ directory, and Git submodules.")
    sys.exit(0)


if __name__ == "__main__":
    run()
