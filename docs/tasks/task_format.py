from typing import TypedDict, List, Literal

try:
    from typing import NotRequired
except ImportError:
    from typing_extensions import NotRequired

Status = Literal["+", "~", "-", "?", "/", "="]

class AcceptanceCriterion(TypedDict):
    phase: str
    criteria: List[str]

class Feature(TypedDict):
    id: str
    feature_id: int
    status: Status
    title: str
    action: str
    acceptance: List[str]
    dependencies: NotRequired[List[str]]
    output: NotRequired[str]
    plan: NotRequired[str]

class Task(TypedDict):
    id: int
    task_id: int
    status: Status
    title: str
    action: str
    acceptance: List[AcceptanceCriterion]
    features: List[Feature]
    plan: NotRequired[str]
