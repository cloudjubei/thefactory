import os
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def run_cmd(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)


def test_orchestrator_scopes_to_child_repo_branch_checkout():
    repo_root = Path(__file__).resolve().parents[2]

    with tempfile.TemporaryDirectory() as tmpdir:
        child_root = Path(tmpdir) / "child_project"
        (child_root / "tasks" / "1").mkdir(parents=True, exist_ok=True)
        # Minimal task with no features to avoid LLM execution
        task = {
            "id": 1,
            "status": "-",
            "title": "Dummy",
            "description": "Dummy child project task",
            "features": []
        }
        (child_root / "tasks" / "1" / "task.json").write_text(json.dumps(task, indent=2))
        (child_root / "README.md").write_text("child project")

        # Initialize a git repo with an initial commit
        run_cmd(["git", "init"], child_root)
        run_cmd(["git", "config", "user.email", "test@example.com"], child_root)
        run_cmd(["git", "config", "user.name", "Test User"], child_root)
        run_cmd(["git", "add", "."], child_root)
        commit_proc = run_cmd(["git", "commit", "-m", "init"], child_root)
        assert commit_proc.returncode == 0, f"Initial commit failed: {commit_proc.stderr}"

        # Run orchestrator via run.py targeting the child repo
        cmd = [
            sys.executable,
            str(repo_root / "run.py"),
            "--agent", "planner",
            "--task", "1",
            "--project-dir", str(child_root)
        ]
        proc = subprocess.run(cmd, text=True, capture_output=True)
        assert proc.returncode == 0, f"orchestrator run failed: stdout={proc.stdout}\nstderr={proc.stderr}"

        # Verify branch operations occurred in child project
        branch_proc = run_cmd(["git", "rev-parse", "--abbrev-ref", "HEAD"], child_root)
        assert branch_proc.returncode == 0, f"Git rev-parse failed: {branch_proc.stderr}"
        assert branch_proc.stdout.strip() == "features/1", f"Expected to be on 'features/1', got '{branch_proc.stdout.strip()}'"
