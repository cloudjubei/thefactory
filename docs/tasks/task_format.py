"""
Defines the canonical data structures for Tasks and Features using Python's typing.
This serves as the schema for the JSON-based task management system.
"""

from typing import List, Literal, TypedDict, Optional

# The status of a task or feature.
# +: Completed
# ~: In Progress
# -: Pending
# ?: Blocked/Question
# /: Deprecated/Cancelled
# =: On Hold
Status = Literal["+", "~", "-", "?", "/", "="]

class Feature(TypedDict):
    """
    Represents a single, actionable feature within a task.
    """
    id: int
    status: Status
    title: str
    action: str
    plan: str # Precise step-by-step plan for this feature. In Markdown format.
    acceptance: str
    context: Optional[List[str]]
    dependencies: Optional[List[str]]
    output: Optional[List[str]]
    notes: Optional[str]
    rejection: Optional[str]
    agent_question: Optional[str] #if the agent asks a question about this feature, it should be stored here.

class Task(TypedDict):
    """
    Represents a single task, containing one or more features.
    This structure is the core of the JSON-based task definition.
    """
    id: int
    status: Status
    title: str
    action: str
    plan: str # High-level intent/plan for the task as a whole. In Markdown format.
    features: List[Feature]
    agent_question: Optional[str] #if the agent asks a question about this task, it should be stored here.
