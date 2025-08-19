from typing import Optional


def finish_feature_tool(git_manager, task_id: int, feature_id: int, title: str, message: Optional[str] = None) -> str:
    """
    Create a per-feature commit and push it to the current branch.

    Args:
        git_manager: An instance of GitManager for the current repo clone.
        task_id: Parent task ID.
        feature_id: Feature index within the task.
        title: Short feature title for the commit subject.
        message: Optional longer description to include in the commit body.

    Returns:
        Status string indicating success or failure.
    """
    if not isinstance(task_id, int) or not isinstance(feature_id, int):
        return "Error: task_id and feature_id must be integers."
    if not isinstance(title, str) or not title.strip():
        return "Error: title must be a non-empty string."

    commit_title = f"Feature {task_id}.{feature_id}: {title.strip()}"
    commit_message = commit_title
    if message and isinstance(message, str) and message.strip():
        commit_message = f"{commit_title}\n\n{message.strip()}"

    if not git_manager.commit_and_push(commit_message=commit_message):
        return "Error: Failed to commit and push feature changes."

    return f"Committed feature {task_id}.{feature_id}: {title.strip()}"