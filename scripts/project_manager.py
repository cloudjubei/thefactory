from pathlib import Path
import os
import shutil
import subprocess
from typing import Optional


def _get_repo_root() -> Path:
    """
    Resolve the repository root directory assuming this file lives at repo_root/scripts/.
    """
    return Path(__file__).resolve().parent.parent


def _safe_text_replace(path: Path, search: str, replace: str) -> None:
    """
    Best-effort text replacement for UTF-8 text files. Binary or undecodable files are skipped.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return
    new_text = text.replace(search, replace)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")


def _run_cmd(args: list[str], cwd: Optional[Path] = None):
    """
    Run a subprocess command in a given working directory. Raises RuntimeError on non-zero exit.
    Kept simple to make it easy to mock in tests.
    """
    result = subprocess.run(args, cwd=str(cwd) if cwd else None)
    rc = getattr(result, "returncode", 0)
    if rc != 0:
        raise RuntimeError(f"Command failed (rc={rc}): {' '.join(args)} in {cwd}")
    return result


def create_child_project(project_name: str) -> Path:
    """
    Create and initialize a child project inside projects/{project_name} using templates/child_project/.
    Steps:
      - Ensure templates exist.
      - Create projects/ and projects/{project_name}.
      - Copy boilerplate files.
      - Replace placeholders like {{PROJECT_NAME}} in text files.
      - Initialize a Git repository in the child project and make an initial commit.
      - Add the child project as a git submodule to the parent repo under projects/{project_name}.

    Returns the created project directory path.
    """
    if not project_name or any(c in project_name for c in "\n\r\t/\\"):
        raise ValueError("Invalid project name.")

    repo_root = _get_repo_root()
    templates_dir = repo_root / "templates" / "child_project"
    if not templates_dir.exists():
        raise FileNotFoundError(f"Templates directory not found: {templates_dir}")

    projects_dir = repo_root / "projects"
    projects_dir.mkdir(parents=True, exist_ok=True)

    target_dir = projects_dir / project_name
    if target_dir.exists():
        raise FileExistsError(f"Child project already exists: {target_dir}")

    # Copy template tree
    shutil.copytree(templates_dir, target_dir)

    # Replace placeholders in text files
    for p in target_dir.rglob("*"):
        if p.is_file():
            _safe_text_replace(p, "{{PROJECT_NAME}}", project_name)

    # Initialize git repository in child project and create initial commit
    _run_cmd(["git", "init"], cwd=target_dir)
    _run_cmd(["git", "add", "."], cwd=target_dir)
    _run_cmd(["git", "commit", "-m", "Initial commit"], cwd=target_dir)

    # Add as submodule to parent repo: git submodule add <path> projects/{project_name}
    rel_submodule_path = str(target_dir.relative_to(repo_root))
    _run_cmd(["git", "submodule", "add", str(target_dir), rel_submodule_path], cwd=repo_root)

    return target_dir


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python scripts/project_manager.py <project_name>")
        sys.exit(1)
    create_child_project(sys.argv[1])
    print("Child project created successfully.")
