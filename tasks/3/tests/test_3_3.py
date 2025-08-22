import os
import stat
import subprocess
import tempfile
from pathlib import Path


def run(cmd, cwd=None, check=True):
    return subprocess.run(cmd, cwd=cwd, check=check, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def make_git_repo(path: Path) -> None:
    run(["git", "init", str(path)])
    # Configure identity for commits
    run(["git", "-C", str(path), "config", "user.email", "test@example.com"]) 
    run(["git", "-C", str(path), "config", "user.name", "Test User"]) 


def make_remote_repo(path: Path) -> str:
    make_git_repo(path)
    (path / "README.md").write_text("remote repo\n")
    run(["git", "-C", str(path), "add", "README.md"]) 
    run(["git", "-C", str(path), "commit", "-m", "init"]) 
    # Determine current branch (main/master depending on git)
    branch = run(["git", "-C", str(path), "rev-parse", "--abbrev-ref", "HEAD"]).stdout.strip()
    return branch


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def script_paths():
    root = project_root()
    scripts_dir = root / "scripts"
    return {
        "init": scripts_dir / "submodules-init.sh",
        "sync": scripts_dir / "submodules-sync.sh",
        "add": scripts_dir / "project-add.sh",
    }


def assert_executable(p: Path):
    assert p.exists(), f"Missing script: {p}"
    st = p.stat()
    assert bool(st.st_mode & stat.S_IXUSR), f"Script not executable: {p}"
    with p.open("r", encoding="utf-8") as fh:
        first = fh.readline().strip()
    assert first == "#!/usr/bin/env sh", f"Script must be POSIX sh with shebang '#!/usr/bin/env sh': {p}"
    # POSIX sh syntax check
    run(["sh", "-n", str(p)])


def test_scripts_exist_and_portable():
    paths = script_paths()
    for p in paths.values():
        assert_executable(p)


def test_help_texts():
    paths = script_paths()
    for key, p in paths.items():
        r = run([str(p), "-h"], check=False)
        assert r.returncode == 0, f"-h must exit 0 for {p}"
        out = r.stdout + r.stderr
        assert "Usage" in out or "usage" in out, f"Help must include Usage for {p}"
        # --help should behave the same
        r2 = run([str(p), "--help"], check=False)
        assert r2.returncode == 0


def test_outside_git_repo_errors_for_repo_required_scripts():
    paths = script_paths()
    with tempfile.TemporaryDirectory() as d:
        dpath = Path(d)
        # init and sync should error outside git repo
        for name in ("init", "sync", "add"):
            r = run([str(paths[name])], cwd=dpath, check=False)
            assert r.returncode != 0, f"{name} must fail outside git repo"
            msg = (r.stdout + r.stderr).lower()
            assert "git" in msg and ("repo" in msg or "repository" in msg), f"{name} must print clear error outside git repo"


def test_init_and_sync_graceful_with_no_submodules():
    paths = script_paths()
    with tempfile.TemporaryDirectory() as d:
        repo = Path(d) / "repo"
        make_git_repo(repo)
        # Ensure no .gitmodules exists
        assert not (repo / ".gitmodules").exists()
        r1 = run([str(paths["init")], cwd=repo, check=False)
        assert r1.returncode == 0, "init must succeed with no submodules"
        r2 = run([str(paths["sync")], cwd=repo, check=False)
        assert r2.returncode == 0, "sync must succeed with no submodules"


def test_project_add_and_submodule_init_flow():
    paths = script_paths()
    with tempfile.TemporaryDirectory() as d:
        dpath = Path(d)
        # Prepare remote repo with one commit
        remote = dpath / "remote"
        branch = make_remote_repo(remote)
        # Prepare parent repo
        parent = dpath / "parent"
        make_git_repo(parent)
        # Run project-add.sh <repo_url> <name> [--branch BRANCH]
        name = "foo"
        cmd = [str(paths["add"]), str(remote), name, "--branch", branch]
        r = run(cmd, cwd=parent, check=False)
        assert r.returncode == 0, f"project-add failed: {r.stdout}\n{r.stderr}"
        # projects/foo must exist and contain README.md
        proj_dir = parent / "projects" / name
        assert proj_dir.exists() and proj_dir.is_dir(), "projects/<name> must be created"
        assert (parent / ".gitmodules").exists(), ".gitmodules must be created"
        gm = (parent / ".gitmodules").read_text()
        assert f"path = projects/{name}" in gm
        assert str(remote) in gm
        # Adding same name again must fail
        r2 = run(cmd, cwd=parent, check=False)
        assert r2.returncode != 0, "Adding duplicate submodule name must fail"
        # Remove working tree of submodule to simulate fresh clone state
        # Then init should repopulate it
        for root, dirs, files in os.walk(proj_dir, topdown=False):
            for f in files:
                (Path(root) / f).unlink()
            for dr in dirs:
                (Path(root) / dr).rmdir()
        # Ensure now empty dir exists
        # Some git versions replace submodule dir with a gitfile; ensure we recreate dir
        proj_dir.mkdir(parents=True, exist_ok=True)
        # Run init script to populate
        r3 = run([str(paths["init")], cwd=parent, check=False)
        assert r3.returncode == 0, f"submodules-init must succeed: {r3.stdout}\n{r3.stderr}"
        # Submodule should contain the README.md from remote
        assert (proj_dir / "README.md").exists(), "Submodule should be checked out after init"
        # Sync should be a no-op but succeed
        r4 = run([str(paths["sync")], cwd=parent, check=False)
        assert r4.returncode == 0


def test_project_add_validates_name_and_path():
    paths = script_paths()
    with tempfile.TemporaryDirectory() as d:
        dpath = Path(d)
        remote = dpath / "remote"
        _branch = make_remote_repo(remote)
        parent = dpath / "parent"
        make_git_repo(parent)
        # Name with slash should fail
        r1 = run([str(paths["add"]), str(remote), "bad/name"], cwd=parent, check=False)
        assert r1.returncode != 0
        # Pre-create path to force 'already exists' failure
        (parent / "projects").mkdir(parents=True, exist_ok=True)
        (parent / "projects" / "exists").mkdir(parents=True, exist_ok=True)
        r2 = run([str(paths["add"]), str(remote), "exists"], cwd=parent, check=False)
        assert r2.returncode != 0
