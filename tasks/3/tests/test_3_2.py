from pathlib import Path


def test_gitignore_rules_for_projects_and_gitmodules():
    repo_root = Path(__file__).resolve().parents[3]
    gitignore_path = repo_root / ".gitignore"

    assert gitignore_path.exists(), ".gitignore must exist at the repository root"

    content = gitignore_path.read_text()
    lines = [line.strip() for line in content.splitlines()]

    # Acceptance criteria 2: includes an ignore rule for projects/
    accepted_project_rules = {"projects/", "/projects/", "projects/**", "/projects/**"}
    assert any(line in accepted_project_rules for line in lines), (
        ".gitignore must include a rule to ignore the projects/ directory"
    )

    # Acceptance criteria 3: explicitly unignore .gitmodules
    accepted_unignore = {"!.gitmodules", "!/.gitmodules"}
    assert any(line in accepted_unignore for line in lines), (
        ".gitignore must explicitly unignore the .gitmodules file"
    )

    # Acceptance criteria 4: must not contain a rule that directly ignores .gitmodules
    disallowed_ignore = {".gitmodules", "/.gitmodules"}
    assert not any(line in disallowed_ignore for line in lines), (
        ".gitignore must not directly ignore .gitmodules"
    )
