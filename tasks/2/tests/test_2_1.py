import os
import tempfile
import subprocess
import importlib.util
from pathlib import Path


def load_git_manager():
    module_path = Path("scripts/git_manager.py").resolve()
    spec = importlib.util.spec_from_file_location("git_manager", str(module_path))
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)  # type: ignore
    return module.GitManager


def run(cmd, cwd=None):
    res = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\nSTDOUT:\n{res.stdout}\nSTDERR:\n{res.stderr}")
    return res


def test_git_manager_exists_and_has_class():
    assert os.path.exists("scripts/git_manager.py"), "scripts/git_manager.py must exist"
    GM = load_git_manager()
    assert GM is not None, "GitManager class should be importable"


def test_git_manager_core_git_operations():
    GM = load_git_manager()

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        bare_repo = tmp_path / "origin.git"
        src_repo = tmp_path / "source"

        # Initialize bare remote repository
        run(["git", "init", "--bare", str(bare_repo)])

        # Initialize source repository and push initial commit to 'main'
        os.makedirs(src_repo, exist_ok=True)
        run(["git", "init"], cwd=src_repo)
        run(["git", "config", "user.email", "tester@example.com"], cwd=src_repo)
        run(["git", "config", "user.name", "Test User"], cwd=src_repo)
        (src_repo / "README.md").write_text("hello\n")
        run(["git", "add", "-A"], cwd=src_repo)
        run(["git", "commit", "-m", "initial"], cwd=src_repo)
        # Ensure branch is 'main'
        run(["git", "branch", "-M", "main"], cwd=src_repo)
        run(["git", "remote", "add", "origin", str(bare_repo)], cwd=src_repo)
        run(["git", "push", "-u", "origin", "main"], cwd=src_repo)

        # Use GitManager to clone and prepare a feature branch
        working_dir = tmp_path / "work"
        gm = GM(repo_url=str(bare_repo), working_dir=str(working_dir))
        ok = gm.setup_repository(branch_name="features/2")
        assert ok, "setup_repository should succeed"
        assert os.path.isdir(os.path.join(gm.repo_path, ".git")), "Repo should be a valid git repository"
        assert gm.current_branch == "features/2", f"Expected to be on 'features/2', got {gm.current_branch}"

        # Make a change, commit and push
        Path(gm.repo_path, "dummy.txt").write_text("data\n")
        assert gm.commit_all("add dummy"), "commit_all should succeed"
        assert gm.push(), "push should succeed"

        # Verify the branch exists on the remote bare repository
        refs = run(["git", "show-ref" ,"--heads" ,"features/2" ,"--" ,str(bare_repo)], cwd=None) if False else subprocess.run(["git", "--git-dir", str(bare_repo), "show-ref", "--heads"], capture_output=True, text=True)
        assert refs.returncode == 0, "Listing refs in bare repo should succeed"
        assert any("refs/heads/features/2" in line for line in refs.stdout.splitlines()), "Remote should have features/2 branch"

        # Create another branch and switch back
        assert gm.create_branch("temp"), "create_branch should succeed"
        assert gm.current_branch == "temp", "Should now be on 'temp' branch"
        assert gm.checkout("features/2"), "checkout to features/2 should succeed"
        assert gm.current_branch == "features/2", "Should be back on features/2"
