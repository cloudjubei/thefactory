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
    This structure is derived from docs/FEATURE_FORMAT.md.
    """
    feature_id: int
    status: Status
    title: str
    action: str
    acceptance: str
    # Optional fields below
    context: Optional[List[str]]
    dependencies: Optional[List[str]]
    output: Optional[List[str]]
    notes: Optional[str]

class Task(TypedDict):
    """
    Represents a single task, containing one or more features.
    This structure is the core of the JSON-based task definition.
    """
    task_id: int
    status: Status
    title: str
    action: str
    acceptance: str
    # Optional fields below
    dependencies: Optional[List[int]]
    plan_intent: str # High-level intent/plan for the task as a whole.
    features: List[Feature]
