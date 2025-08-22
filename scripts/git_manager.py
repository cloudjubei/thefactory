import subprocess
from typing import List

class GitManager:
    """A class to interact with a git repository."""

    def __init__(self, repo_path: str = "."):
        """
        Initializes the GitManager.

        :param repo_path: The path to the git repository.
        """
        self.repo_path = repo_path
        self.configure()

    def configure(self):
        self._run_command(["config", "--local", "user.name", "AI Agent"])
        self._run_command(["config", "--local", "user.email", "ai@agent.com"])

    def _run_command(self, command: List[str]) -> str:
        """
        Runs a git command and returns the output.

        :param command: The command to run as a list of strings.
        :return: The output of the command.
        """
        try:
            result = subprocess.run(
                ["git", "-C", self.repo_path] + command,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Git command failed: {e.stderr.strip()} (stdout: {e.stdout.strip()})") from e

    def stage_files(self, files: List[str]):
        """
        Stages the given files.

        :param files: A list of file paths to stage.
        """
        self._run_command(["add"] + files)

    def commit(self, message: str) -> str:
        """
        Commits the staged changes, handling the case where there is nothing to commit.

        :param message: The commit message.
        """
        try:
            result = subprocess.run(
                ["git", "-C", self.repo_path, "commit", "-m", message],
                capture_output=True,
                text=True,
                check=False
            )
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                full_output = (result.stdout + result.stderr).lower()
                if "nothing to commit" in full_output or "no changes added to commit" in full_output:
                    return "Nothing to commit."
                else:
                    raise RuntimeError(f"Git commit failed: {result.stderr.strip()} (stdout: {result.stdout.strip()})")
        except Exception as e:
            raise RuntimeError(f"Unexpected error in commit: {e}") from e

    def push(self, remote: str = "origin", branch: str = "main"):
        """
        Pushes the changes to the remote repository.

        :param remote: The name of the remote repository.
        :param branch: The branch to push to.
        """
        self._run_command(["push", remote, branch])

    def get_current_branch(self) -> str:
        """
        Gets the current active branch name.

        :return: The name of the current branch.
        """
        return self._run_command(["rev-parse", "--abbrev-ref", "HEAD"])

    def create_branch_and_checkout(self, branch_name: str, remote: str = "origin"):
        """
        Creates and checks out a new branch.

        :param branch_name: The name of the branch to create.
        """
        self._run_command(["checkout", "-b", branch_name])
        
        self._run_command(["pull", remote, branch_name])
        