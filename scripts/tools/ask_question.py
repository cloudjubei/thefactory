def ask_question_tool(question_text: str) -> str:
    """
    Signal to the orchestrator that human input is required. This halts continuous execution.
    Returns a HALT string the orchestrator recognizes.
    """
    if not isinstance(question_text, str) or not question_text.strip():
        return "HALT: QUESTION: (empty question)"
    return f"HALT: QUESTION: {question_text}"
