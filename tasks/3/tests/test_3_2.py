import os


def test_gitignore_projects_and_gitmodules():
    repo_root = os.getcwd()
    gitignore_path = os.path.join(repo_root, ".gitignore")

    # 1. .gitignore exists at the repository root.
    assert os.path.isfile(gitignore_path), (
        "Acceptance Criterion 1 failed: .gitignore must exist at the repository root."
    )

    # Read and normalize .gitignore lines (strip whitespace, remove empty and comment-only lines)
    with open(gitignore_path, "r", encoding="utf-8") as f:
        raw_lines = f.read().splitlines()

    lines = []
    for line in raw_lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            continue
        lines.append(stripped)

    # 2. Check for acceptable projects/ ignore patterns
    allowed_projects_patterns = {"projects/", "/projects/", "projects/**", "/projects/**"}
    has_projects_ignore = any(l in allowed_projects_patterns for l in lines)
    assert has_projects_ignore, (
        "Acceptance Criterion 2 failed: .gitignore must include an ignore rule for the entire projects/ "
        "directory and its contents. Expected one of: " + ", ".join(sorted(allowed_projects_patterns))
    )

    # 3. Check explicit unignore for .gitmodules
    unignore_gitmodules_patterns = {"!.gitmodules", "!/.gitmodules"}
    has_unignore_gitmodules = any(l in unignore_gitmodules_patterns for l in lines)
    assert has_unignore_gitmodules, (
        "Acceptance Criterion 3 failed: .gitignore must explicitly unignore .gitmodules using one of: "
        + ", ".join(sorted(unignore_gitmodules_patterns))
    )

    # 4. Ensure no direct ignore rule for .gitmodules
    disallowed_gitmodules_ignore = {".gitmodules", "/.gitmodules"}
    has_disallowed = any(l in disallowed_gitmodules_ignore for l in lines)
    assert not has_disallowed, (
        "Acceptance Criterion 4 failed: .gitignore must not directly ignore .gitmodules; found one of: "
        + ", ".join(sorted(disallowed_gitmodules_ignore))
    )
