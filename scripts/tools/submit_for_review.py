from typing import Optional


def submit_for_review_tool(git_manager, task_id: int, task_title: str) -> str:
    """
    Commit all changes, switch to a features/{task_id} branch, push, and open a PR to main.

    Args:
        git_manager: An instance of GitManager managing the current repo clone.
        task_id: The ID of the task being submitted.
        task_title: The title of the task being submitted.

    Returns:
        A human-readable status string indicating success/failure.
    """
    if not isinstance(task_id, int):
        return "Error: task_id must be an integer."
    if not isinstance(task_title, str) or not task_title.strip():
        return "Error: task_title must be a non-empty string."

    branch_name = f"features/{task_id}"
    commit_message = f"Task {task_id}: {task_title}"
    pr_title = commit_message
    pr_body = (
        f"Automated submission for Task {task_id}: {task_title}.\n\n"
        "This PR was created by the orchestrator via submit_for_review.\n"
        "- Changes include files created/updated by the agent for this task.\n"
        "- Branch naming follows features/{task_id}.\n"
        "- Base branch: main.\n"
    )

    # Ensure we are on a dedicated feature branch
    if not git_manager._run_command(["git", "checkout", "-B", branch_name]):
        return f"Error: Failed to switch to branch {branch_name}."
    
    if not git_manager._run_command(["git", "pull"]):
        return f"Error: Failed to pull branch {branch_name}."

    # Commit and push changes
    if not git_manager.commit_and_push(commit_message=commit_message):
        return "Error: Failed to commit and push changes."

    # Create PR
    if not git_manager.create_pull_request(title=pr_title, body=pr_body):
        return "Error: Failed to create pull request. Ensure GitHub CLI is installed and authenticated (gh auth login)."

    return f"Submitted PR for Task {task_id}: {task_title} on branch {branch_name}."
