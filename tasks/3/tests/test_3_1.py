import sys
import subprocess
from pathlib import Path


def run_script(args, cwd=None):
    repo_root = Path(__file__).resolve().parents[3]
    script_path = repo_root / "scripts" / "child_project_utils.py"
    cmd = [sys.executable, str(script_path)] + args
    return subprocess.run(cmd, cwd=cwd or repo_root, capture_output=True, text=True)


def test_help_shows_task_id():
    proc = run_script(["-h"])  # argparse exits 0 with help
    assert proc.returncode == 0
    # argparse writes help to stdout
    assert "--task-id" in proc.stdout


def test_dry_run_plan_contains_expected_actions(tmp_path):
    # Run in isolated tmp working dir
    proj_name = "my-child-proj"
    proc = run_script([proj_name, "--dry-run"], cwd=tmp_path)
    assert proc.returncode == 0, proc.stderr

    out = proc.stdout
    # Planned directories and files
    assert f"Create directory: projects" in out
    assert f"Create directory: projects/{proj_name}" in out
    assert f"Create directory: projects/{proj_name}/tasks" in out
    assert f"Create directory: projects/{proj_name}/tasks/1" in out
    assert f"Create file: projects/{proj_name}/README.md" in out
    assert f"Create file: projects/{proj_name}/.gitignore" in out
    assert f"Create file: projects/{proj_name}/tasks/1/task.json" in out

    # Planned git commands
    assert "CMD: git init" in out
    assert "CMD: git add ." in out
    assert "CMD: git commit -m" in out
    assert "CMD: git submodule add" in out


def test_existing_target_fails_fast(tmp_path):
    # Pre-create the target directory to simulate collision
    projects_dir = tmp_path / "projects"
    projects_dir.mkdir(parents=True)
    target_dir = projects_dir / "already-exists"
    target_dir.mkdir()

    proc = run_script(["already-exists", "--dry-run"], cwd=tmp_path)
    assert proc.returncode != 0
    assert "already exists" in proc.stderr


def test_rewrite_task_ids_function():
    # Import the module to access the helper
    repo_root = Path(__file__).resolve().parents[3]
    sys.path.insert(0, str(repo_root / "scripts"))
    try:
        import child_project_utils as mod
    finally:
        sys.path.pop(0)

    sample = {
        "id": 13,
        "features": [
            {"id": "13.1", "title": "A"},
            {"id": "13.10", "title": "B"},
            {"id": "no-dot", "title": "C"},
        ],
    }
    out = mod.rewrite_task_ids(sample, new_id=1)
    assert out["id"] == 1
    fids = [f["id"] for f in out["features"]]
    assert fids == ["1.1", "1.10", "no-dot"]
