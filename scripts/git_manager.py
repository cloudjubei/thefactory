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
            raise RuntimeError(f"Git command failed: {e.stderr}") from e

    def stage_files(self, files: List[str]):
        """
        Stages the given files.

        :param files: A list of file paths to stage.
        """
        self._run_command(["add"] + files)

    def commit(self, message: str):
        """
        Commits the staged changes.

        :param message: The commit message.
        """
        self._run_command(["commit", "-m", message])

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