def finish_tool(git_manager, reason: str) -> str:
    """
    Signal that the agent's current cycle is complete. In continuous mode,
    the orchestrator will start a new cycle unless the reason indicates a halt.
    """
    if not isinstance(reason, str) or not reason.strip():
        reason = "Completed current cycle."
    if not git_manager.commit_and_push(commit_message=reason):
        return "Error: Failed to commit and push finish changes."
    return f"HALT: {reason}"
