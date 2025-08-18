def finish_tool(reason: str) -> str:
    """
    Signal that the agent's current cycle is complete. In continuous mode,
    the orchestrator will start a new cycle unless the reason indicates a halt.
    """
    if not isinstance(reason, str) or not reason.strip():
        reason = "Completed current cycle."
    return f"HALT: {reason}"
