import os
import subprocess
from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class GitCommandResult:
    ok: bool
    stdout: str
    stderr: str
    returncode: int


class GitManager:
    """
    A small wrapper around git CLI for repository operations.

    Responsibilities:
    - Clone or reuse a working repository directory.
    - Create and checkout branches.
    - Commit and push changes.
    - Provide basic utilities for git command execution.

    Notes:
    - Designed to work with local paths or remote URLs.
    - Avoids external dependencies: uses subprocess to call git.
    - Safe defaults for user.name and user.email if not configured.
    """

    def __init__(self, repo_url: str, working_dir: str, default_branch: Optional[str] = None):
        self.repo_url = repo_url
        self.working_dir = os.path.abspath(working_dir)
        self._default_branch = default_branch

    # ---------- Public properties ----------
    @property
    def repo_path(self) -> str:
        """Path to the repository working directory (clone target)."""
        return self.working_dir

    @property
    def current_branch(self) -> Optional[str]:
        res = self._run_git(["rev-parse", "--abbrev-ref", "HEAD"]) if self._is_git_repo() else GitCommandResult(False, "", "", 1)
        return res.stdout.strip() if res.ok else None

    # ---------- Core setup ----------
    def setup_repository(self, branch_name: str) -> bool:
        """
        Ensure a usable repository is available at working_dir and that branch_name
        exists and is checked out. Returns True on success.
        """
        os.makedirs(self.working_dir, exist_ok=True)

        if not self._is_git_repo():
            # Clone into working_dir
            clone_res = self._run(["git", "clone", self.repo_url, self.working_dir], cwd=None)
            if not clone_res.ok:
                return False
        else:
            # Fetch latest
            self._run_git(["fetch", "--all", "--prune"])  # Best effort

        # Ensure basic config
        self._ensure_user_config()

        # Determine default branch
        default_branch = self.get_default_branch()

        # Create and/or checkout the requested feature branch
        if not self._branch_exists(branch_name):
            # Try create from origin/default or local default
            base_ref = f"origin/{default_branch}" if self._remote_branch_exists(default_branch) else default_branch
            create_res = self._run_git(["checkout", "-b", branch_name, base_ref])
            if not create_res.ok:
                # Fallback: create empty branch if base_ref missing
                create_empty = self._run_git(["checkout", "--orphan", branch_name])
                if not create_empty.ok:
                    return False
                # Ensure at least one commit can exist later
        else:
            co_res = self._run_git(["checkout", branch_name])
            if not co_res.ok:
                return False

        return True

    # ---------- Common actions ----------
    def commit_all(self, message: str) -> bool:
        add_res = self._run_git(["add", "-A"]) if self._is_git_repo() else GitCommandResult(False, "", "", 1)
        if not add_res.ok:
            return False
        commit_res = self._run_git(["commit", "-m", message, "--allow-empty"])
        return commit_res.ok

    def push(self, branch_name: Optional[str] = None, set_upstream: bool = True) -> bool:
        if not self._is_git_repo():
            return False
        if branch_name is None:
            branch_name = self.current_branch
        if not branch_name:
            return False
        args = ["push", "origin", branch_name]
        if set_upstream:
            args.insert(1, "-u")
        res = self._run_git(args)
        return res.ok

    def create_branch(self, name: str, from_ref: Optional[str] = None) -> bool:
        if not self._is_git_repo():
            return False
        if from_ref is None:
            from_ref = self.get_default_branch()
            if self._remote_branch_exists(from_ref):
                from_ref = f"origin/{from_ref}"
        res = self._run_git(["checkout", "-b", name, from_ref])
        return res.ok

    def checkout(self, ref: str) -> bool:
        if not self._is_git_repo():
            return False
        res = self._run_git(["checkout", ref])
        return res.ok

    # ---------- Helpers ----------
    def get_default_branch(self) -> str:
        """
        Resolve the repository's default branch.
        Strategy:
        1) origin/HEAD -> origin/<branch>
        2) If origin/main exists -> main
        3) Else fallback to master
        """
        if self._is_git_repo():
            head_res = self._run_git(["symbolic-ref", "--short", "refs/remotes/origin/HEAD"])  # e.g., origin/main
            if head_res.ok:
                value = head_res.stdout.strip()
                if value.startswith("origin/"):
                    return value.split("/", 1)[1]
            # Check common names
            if self._remote_branch_exists("main"):
                return "main"
            return "master"
        # If not yet a repo, best guess
        return self._default_branch or "main"

    def _is_git_repo(self) -> bool:
        return os.path.isdir(os.path.join(self.working_dir, ".git"))

    def _branch_exists(self, name: str) -> bool:
        res = self._run_git(["rev-parse", "--verify", name]) if self._is_git_repo() else GitCommandResult(False, "", "", 1)
        return res.ok

    def _remote_branch_exists(self, name: str) -> bool:
        if not self._is_git_repo():
            return False
        res = self._run_git(["ls-remote", "--heads", "origin", name])
        return res.ok and bool(res.stdout.strip())

    def _ensure_user_config(self) -> None:
        # Ensure git user.email and user.name inside the repo
        email = self._git_config_get("user.email")
        name = self._git_config_get("user.name")
        if not email:
            self._run_git(["config", "user.email", os.environ.get("GIT_USER_EMAIL", "agent@example.com")])
        if not name:
            self._run_git(["config", "user.name", os.environ.get("GIT_USER_NAME", "Automation Agent")])

    def _git_config_get(self, key: str) -> Optional[str]:
        res = self._run_git(["config", "--get", key]) if self._is_git_repo() else GitCommandResult(False, "", "", 1)
        if res.ok:
            return res.stdout.strip() or None
        return None

    # ---------- Low-level invocation ----------
    def _run_git(self, args: list[str]) -> GitCommandResult:
        return self._run(["git", *args], cwd=self.working_dir)

    def _run(self, cmd: list[str], cwd: Optional[str]) -> GitCommandResult:
        try:
            proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)
            ok = proc.returncode == 0
            return GitCommandResult(ok=ok, stdout=proc.stdout, stderr=proc.stderr, returncode=proc.returncode)
        except Exception as e:
            return GitCommandResult(ok=False, stdout="", stderr=str(e), returncode=1)
