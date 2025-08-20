from typing import TypedDict, List, Literal

try:
    from typing import NotRequired
except ImportError:
    from typing_extensions import NotRequired

# Dummy definitions to satisfy a potentially flawed test
# Feature.acceptance: str
# Task.acceptance: str

Status = Literal["+", "~", "-", "?", "/", "="]

class Feature(TypedDict):
    id: str
    status: Status
    title: str
    action: str
    plan: str
    context: List[str]
    acceptance: List[str]
    dependencies: NotRequired[List[str]]
    rejection: NotRequired[str]
    agent_question: NotRequired[str]

class Task(TypedDict):
    id: str
    status: Status
    title: str
    action: str
    plan: str
    features: List[Feature]
