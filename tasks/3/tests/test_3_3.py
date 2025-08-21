import os, sys


def fail(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)


def run():
    base_dir = os.path.join("templates", "child_project")
    if not os.path.isdir(base_dir):
        fail(f"Directory '{base_dir}' does not exist.")

    files = [
        ("README.md", True),
        (".gitignore", True),
        ("spec.md", True),
    ]

    for fname, must_exist in files:
        path = os.path.join(base_dir, fname)
        if must_exist and not os.path.exists(path):
            fail(f"Required file missing: {path}")

    # Validate README.md content
    readme_path = os.path.join(base_dir, "README.md")
    with open(readme_path, "r", encoding="utf-8") as f:
        readme = f.read()
    required_readme_markers = [
        "{{PROJECT_NAME}}",
        "# ",  # has a title
        "submodule",  # mentions submodule linkage
        "projects/",  # mentions projects dir in parent
    ]
    missing_readme = [m for m in required_readme_markers if m not in readme]
    if missing_readme:
        fail("README.md is missing required markers: " + ", ".join(missing_readme))

    # Validate spec.md content
    spec_path = os.path.join(base_dir, "spec.md")
    with open(spec_path, "r", encoding="utf-8") as f:
        spec = f.read()
    required_spec_markers = [
        "Specification: {{PROJECT_NAME}}",
        "## 1. Purpose",
        "## 3. Requirements",
        "projects/{{PROJECT_NAME}}",
    ]
    missing_spec = [m for m in required_spec_markers if m not in spec]
    if missing_spec:
        fail("spec.md is missing required sections/markers: " + ", ".join(missing_spec))

    # Validate .gitignore has generic entries
    gi_path = os.path.join(base_dir, ".gitignore")
    with open(gi_path, "r", encoding="utf-8") as f:
        gi = f.read()
    required_gitignore = ["__pycache__/", "node_modules/", ".DS_Store"]
    missing_gi = [m for m in required_gitignore if m not in gi]
    if missing_gi:
        fail(".gitignore missing generic patterns: " + ", ".join(missing_gi))

    print("PASS: Child project boilerplate templates exist with suitable content.")
    sys.exit(0)


if __name__ == "__main__":
    run()
