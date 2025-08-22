import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
import json

# Helper to run commands capturing output

def run(cmd, cwd=None, check=True):
    res = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if check and res.returncode != 0:
        raise AssertionError(f"Command failed: {' '.join(cmd)}\ncode={res.returncode}\nstdout=\n{res.stdout}\nstderr=\n{res.stderr}")
    return res


def has_git():
    try:
        run(["git", "--version"], check=True)
        return True
    except AssertionError:
        return False


def test_generate_child_project_end_to_end():
    if not has_git():
        # Skip if git not available in CI env
        print("SKIP: git not available")
        return

    repo_root = Path.cwd()

    # Try to detect the generator script path
    candidate_scripts = [
        repo_root / "scripts" / "generate_child_project.py",
        repo_root / "scripts" / "child_projects.py",
        repo_root / "scripts" / "children.py",
        repo_root / "generate_child_project.py",
    ]
    generator = None
    for c in candidate_scripts:
        if c.exists():
            generator = c
            break
    assert generator is not None, "Generator script not found; expected one of: scripts/generate_child_project.py, scripts/child_projects.py, generate_child_project.py"

    # Use a temp working clone of the current repo to avoid mutating the real repo during the test
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        # Initialize a new git repo and add a remote to the current repo if applicable; alternatively copy minimal files
        run(["git", "init", "--initial-branch=main"], cwd=tmp)

        # Copy only what's necessary: scripts/, .gitignore if exists, and minimal files to allow running the script
        items_to_copy = ["scripts", ".gitignore", "pyproject.toml", "README.md", "requirements.txt"]
        for item in items_to_copy:
            src = repo_root / item
            if src.exists():
                dst = tmp / item
                if src.is_dir():
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)

        # Ensure projects/ exists
        (tmp / "projects").mkdir(parents=True, exist_ok=True)

        # Commit baseline
        run(["git", "add", "-A"], cwd=tmp)
        run(["git", "commit", "-m", "test: baseline"], cwd=tmp)

        # Determine runner (python -m vs direct)
        if generator.name.endswith(".py"):
            cmd_base = [sys.executable, str(generator.relative_to(repo_root))]
        else:
            cmd_base = [str(generator.relative_to(repo_root))]

        project_name = "feature_demo_proj"
        child_path = tmp / "projects" / project_name

        # 1) Dry run creates no changes
        res = run(cmd_base + ["--name", project_name, "--dry-run"], cwd=tmp)
        assert res.returncode == 0
        assert not child_path.exists(), "Dry-run should not create the child directory"
        # Ensure .gitmodules unchanged and working tree clean
        git_status = run(["git", "status", "--porcelain"], cwd=tmp)
        assert git_status.stdout.strip() == "", f"Dry-run must not modify the repo, got changes: {git_status.stdout}"

        # 2) Real run creates structure and submodule
        res = run(cmd_base + ["--name", project_name, "--description", "Test child project"], cwd=tmp)
        assert res.returncode == 0

        # Validate filesystem structure
        assert child_path.exists() and child_path.is_dir(), "Child project directory should be created"
        assert (child_path / "README.md").exists(), "README.md should be present"
        assert (child_path / "tasks").exists(), "tasks/ directory should be present"
        # initial task: accept common names
        initial_tasks = list((child_path / "tasks").glob("*initial*task*.*")) or list((child_path / "tasks").glob("000_*"))
        assert initial_tasks, "An initial task file should be created in tasks/"
        # child .git repo exists
        assert (child_path / ".git").exists(), "Child project should be an independent git repository"
        # child git has initial commit and clean status
        child_log = run(["git", "log", "--oneline"], cwd=child_path)
        assert child_log.stdout.strip() != "", "Child repo should have an initial commit"
        child_status = run(["git", "status", "--porcelain"], cwd=child_path)
        assert child_status.stdout.strip() == "", "Child repo should be clean after initial commit"

        # Root repo has submodule entry
        gitmodules = tmp / ".gitmodules"
        assert gitmodules.exists(), ".gitmodules should be created/updated with the submodule"
        gm = gitmodules.read_text()
        assert f"path = projects/{project_name}" in gm, "Submodule path should be registered in .gitmodules"

        # Verify it's a gitlink in the root index
        sub_status = run(["git", "ls-files", "--stage", f"projects/{project_name}"], cwd=tmp)
        # Mode 160000 indicates gitlink (submodule)
        assert "160000" in sub_status.stdout, "Child project should be added as a submodule (gitlink) in the root repo"

        # 3) Idempotency / duplicate project name should fail without changes
        pre_status = run(["git", "status", "--porcelain"], cwd=tmp).stdout
        res_dup = subprocess.run(cmd_base + ["--name", project_name], cwd=tmp, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        assert res_dup.returncode != 0, "Re-running for the same project should fail with non-zero exit"
        post_status = run(["git", "status", "--porcelain"], cwd=tmp).stdout
        assert pre_status == post_status, "Duplicate attempt should not modify the repository state"

        # 4) Remote origin optional: set a dummy URL and ensure child origin set
        project_name2 = "feature_demo_proj_remote"
        res2 = run(cmd_base + ["--name", project_name2, "--repo-url", "https://example.com/org/feature_demo_proj_remote.git"], cwd=tmp)
        assert res2.returncode == 0
        child2 = tmp / "projects" / project_name2
        assert child2.exists()
        origin2 = run(["git", "remote", "get-url", "origin"], cwd=child2)
        assert origin2.stdout.strip().endswith("feature_demo_proj_remote.git"), "Child repo should have origin set when repo_url provided"

        # 5) Help/usage output
        help_ok = False
        for flag in ("-h", "--help"):
            proc = subprocess.run(cmd_base + [flag], cwd=tmp, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if proc.returncode == 0 and ("Usage" in proc.stdout or "usage" in proc.stdout or "--name" in proc.stdout):
                help_ok = True
                break
        assert help_ok, "Help/usage should be available via -h/--help"
