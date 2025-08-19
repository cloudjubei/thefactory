# scripts/git_manager.py

import subprocess
import sys
import os

class GitManager:
    """A class to handle basic git operations for the autonomous agent."""

    def __init__(self, repo_url: str, working_dir: str = "/tmp/agent_repo"):
        """
        Initializes the GitManager.

        Args:
            repo_url (str): The URL of the git repository.
            working_dir (str): The local directory to clone the repo into.
        """
        self.repo_url = repo_url
        self.working_dir = working_dir
        self.repo_path = os.path.join(self.working_dir, os.path.basename(repo_url).replace('.git', ''))

    def _run_command(self, command: list[str], cwd: str = None):
        """
        Runs a shell command and handles errors.

        Args:
            command (list[str]): The command to run as a list of strings.
            cwd (str, optional): The directory to run the command in. Defaults to None.

        Returns:
            bool: True if the command was successful, False otherwise.
        """
        print(f"Executing command: {' '.join(command)}")
        try:
            subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
                cwd=cwd or self.repo_path
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {' '.join(command)}", file=sys.stderr)
            print(f"Stderr: {e.stderr}", file=sys.stderr)
            print(f"Stdout: {e.stdout}", file=sys.stderr)
            return False

    def setup_repository(self, branch_name: str = "main") -> bool:
        """
        Clones the repository, fetches latest changes, and creates a new branch.

        Args:
            branch_name (str): The name of the new branch to create.

        Returns:
            bool: True if setup was successful, False otherwise.
        """
        if os.path.exists(self.working_dir):
            print(f"Cleaning up existing working directory: {self.working_dir}")
            if not self._run_command(["rm", "-rf", self.working_dir], cwd="/"):
                return False
        
        if not self._run_command(["git", "clone", self.repo_url, self.repo_path], cwd="/"):
            return False
            
        if not self._run_command(["git", "checkout", "main"]): return False
        if not self._run_command(["git", "pull"]): return False
        if (branch_name != "main"):
            if not self._run_command(["git", "checkout", "-b", branch_name]): return False
            if not self._run_command(["git", "pull"]): return False
            
        print(f"Successfully created and checked out branch '{branch_name}' in '{self.repo_path}'")
        return True

    def commit_and_push(self, commit_message: str) -> bool:
        """
        Adds all changes, commits them, and pushes the branch to origin.

        Args:
            commit_message (str): The commit message.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        branch_name = self._get_current_branch()
        if not branch_name: return False
            
        if not self._run_command(["git", "add", "."]): return False
        if not self._run_command(["git", "commit", "-m", commit_message]):
            print("Warning: `git commit` failed. This may be because there were no changes to commit.")
        if not self._run_command(["git", "push", "-u", "origin", branch_name]): return False
            
        print(f"Successfully committed and pushed branch '{branch_name}' to origin.")
        return True
        
    def create_pull_request(self, title: str, body: str) -> bool:
        """
        Creates a pull request using the GitHub CLI.

        Args:
            title (str): The title of the pull request.
            body (str): The body content of the pull request.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        command = ["gh", "pr", "create", "--title", title, "--body", body, "--base", "main"]
        if not self._run_command(command):
            print("Error: Failed to create pull request. Ensure 'gh' is installed and authenticated ('gh auth login').", file=sys.stderr)
            return False
        
        if not self._run_command(["rm", "-rf", self.working_dir], cwd="/"):
            print("Error: Failed to cleanup tmp repository.", file=sys.stderr)
            return False
        
        print(f"Successfully created pull request with title: '{title}'")
        return True

    def _get_current_branch(self) -> str:
        """Helper to get the current git branch."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                check=True, capture_output=True, text=True, cwd=self.repo_path
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            print("Error: Could not determine current branch.", file=sys.stderr)
            return ""

if __name__ == '__main__':
    # This example demonstrates the full local workflow.
    
    if len(sys.argv) != 5:
        print("Usage: python3 git_manager.py <REPO_URL> <BRANCH_NAME> <COMMIT_MESSAGE> \"<PR_BODY>\"")
        sys.exit(1)
        
    repo_url_arg = sys.argv[1]
    branch_name_arg = sys.argv[2]
    commit_message_arg = sys.argv[3]
    pr_body_arg = sys.argv[4]
    
    manager = GitManager(repo_url=repo_url_arg)
    
    # Step 1: Setup repository and branch
    if not manager.setup_repository(branch_name=branch_name_arg): sys.exit(1)
        
    # Step 2: In a real scenario, the agent would now modify files.
    # For this example, we create a dummy file.
    with open(os.path.join(manager.repo_path, "agent_test_file.txt"), "w") as f:
        f.write(f"This is a test file for branch {branch_name_arg}.\n")

    # Step 3: Commit and push changes
    if not manager.commit_and_push(commit_message=commit_message_arg): sys.exit(1)

    # Step 4: Create pull request
    if not manager.create_pull_request(title=commit_message_arg, body=pr_body_arg): sys.exit(1)

    print("\nGit and GitHub operations completed successfully.")