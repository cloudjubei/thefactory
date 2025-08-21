import os
import subprocess
from typing import Optional, Tuple


class GitManager:
    """
    Lightweight Git helper used by agent tools to interact with repositories.

    Responsibilities:
    - Clone/setup a working repository in a given directory.
    - Create/check out branches.
    - Stage and commit changes.
    - Push branches/tags to origin.

    Notes:
    - This manager relies on the system `git` CLI via subprocess for portability.
    - Networked operations (push, PR creation) are best-effort and should fail gracefully.
    """

    def __init__(self, repo_url: str, working_dir: str):
        self.repo_url = repo_url
        self.working_dir = working_dir
        self.repo_path = working_dir

    # --------------------------
    # Internal helpers
    # --------------------------
    def _run(self, *args: str, cwd: Optional[str] = None, check: bool = False) -> Tuple[int, str, str]:
        """Run a git (or other) command. Returns (returncode, stdout, stderr)."""
        proc = subprocess.run(
            list(args),
            cwd=cwd or self.repo_path,
            capture_output=True,
            text=True,
        )
        if check and proc.returncode != 0:
            raise subprocess.CalledProcessError(proc.returncode, args, output=proc.stdout, stderr=proc.stderr)
        return proc.returncode, proc.stdout.strip(), proc.stderr.strip()

    def _git(self, *git_args: str, cwd: Optional[str] = None, check: bool = False) -> Tuple[int, str, str]:
        return self._run("git", *git_args, cwd=cwd, check=check)

    # --------------------------
    # Public API
    # --------------------------
    def ensure_user_config(self, name: str = "AI Agent", email: str = "agent@example.com") -> bool:
        """Ensure git user.name and user.email are configured locally for this repo."""
        rc_name, out_name, _ = self._git("config", "user.name")
        rc_email, out_email, _ = self._git("config", "user.email")
        changed = False
        if rc_name != 0 or not out_name:
            self._git("config", "user.name", name)
            changed = True
        if rc_email != 0 or not out_email:
            self._git("config", "user.email", email)
            changed = True
        return changed

    def setup_repository(self, branch_name: str = "main") -> bool:
        """
        Prepare the working directory as a git repository:
        - If not already a git repo, clone repo_url into working_dir.
        - Fetch remotes, create/checkout the specified branch.
        - Ensure user config exists.
        Returns True on success, False otherwise.
        """
        os.makedirs(self.working_dir, exist_ok=True)
        # If not a repo yet, clone
        if not os.path.isdir(os.path.join(self.repo_path, ".git")):
            rc, _, err = self._git("clone", self.repo_url, self.repo_path, cwd="/")
            # Some git versions require running from a different cwd for clone
            if rc != 0:
                # Fallback attempt: run from working_dir's parent
                parent = os.path.dirname(os.path.abspath(self.repo_path)) or "/"
                os.makedirs(parent, exist_ok=True)
                rc, _, err = self._git("clone", self.repo_url, self.repo_path, cwd=parent)
                if rc != 0:
                    return False
        # Ensure we operate inside the repo
        # Fetch and checkout/create branch
        self._git("fetch", "--all")
        # Try to checkout existing branch, else create it
        rc, _, _ = self._git("checkout", branch_name)
        if rc != 0:
            rc, _, _ = self._git("checkout", "-b", branch_name)
            if rc != 0:
                return False
        self.ensure_user_config()
        return True

    def create_branch(self, branch_name: str, checkout: bool = True) -> bool:
        rc, _, _ = self._git("branch", "--list", branch_name)
        # Always attempt to create; git will fail if exists
        rc_create, _, _ = self._git("branch", branch_name)
        # If requested, checkout
        if checkout:
            rc_co, _, _ = self._git("checkout", branch_name)
            return rc_co == 0
        return rc_create == 0 or rc == 0

    def checkout_branch(self, branch_name: str) -> bool:
        rc, _, _ = self._git("checkout", branch_name)
        return rc == 0

    def current_branch(self) -> Optional[str]:
        rc, out, _ = self._git("rev-parse", "--abbrev-ref", "HEAD")
        return out if rc == 0 else None

    def commit_all(self, message: str = "chore: automated update") -> bool:
        self._git("add", "-A")
        # Commit only if there are staged changes
        rc_diff, out_diff, _ = self._git("diff", "--cached", "--name-only")
        if rc_diff != 0 or not out_diff:
            return False
        rc, _, _ = self._git("commit", "-m", message)
        return rc == 0

    def push_branch(self, branch_name: Optional[str] = None, set_upstream: bool = True) -> bool:
        if branch_name is None:
            branch_name = self.current_branch() or "main"
        args = ["push", "origin", branch_name]
        if set_upstream:
            args.insert(1, "-u")
        rc, _, _ = self._git(*args)
        return rc == 0

    def tag(self, tag_name: str, message: Optional[str] = None) -> bool:
        if message:
            rc, _, _ = self._git("tag", "-a", tag_name, "-m", message)
        else:
            rc, _, _ = self._git("tag", tag_name)
        return rc == 0

    def push_tags(self) -> bool:
        rc, _, _ = self._git("push", "--tags")
        return rc == 0

    def pull_rebase(self) -> bool:
        rc, _, _ = self._git("pull", "--rebase")
        return rc == 0

    def merge(self, source_branch: str) -> bool:
        rc, _, _ = self._git("merge", source_branch)
        return rc == 0

    def get_repo_url(self) -> str:
        rc, out, _ = self._git("config", "--get", "remote.origin.url")
        return out if rc == 0 else self.repo_url

    # Optional: Provide a no-op PR creation to satisfy tool interfaces without external deps
    def create_pull_request(self, title: str, body: str = "", base: str = "main", head: Optional[str] = None) -> str:
        """
        Best-effort PR creation. If GitHub CLI `gh` is available and a token is configured,
        it will attempt to create a PR. Otherwise, it returns a message describing what would happen.
        Returns a string message/URL when possible.
        """
        head = head or (self.current_branch() or "")
        # Try GitHub CLI
        rc, _, _ = self._run("gh", "--version")
        if rc == 0 and head:
            args = [
                "gh", "pr", "create",
                "--title", title,
                "--body", body or title,
                "--base", base,
                "--head", head,
            ]
            rc2, out2, err2 = self._run(*args)
            if rc2 == 0 and out2:
                return out2
            return f"Failed to create PR via gh: {err2 or 'unknown error'}"
        return f"PR requested (base={base}, head={head}) - gh CLI not available; skipping creation."

    # Backwards-compatible alias some tools might expect
    open_pull_request = create_pull_request
