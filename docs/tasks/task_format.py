from typing import TypedDict, List

try:
    from typing import NotRequired
except ImportError:
    from typing_extensions import NotRequired

class AcceptanceCriterion(TypedDict):
    phase: str
    criteria: List[str]

class Feature(TypedDict):
    id: str
    feature_id: int # Added to satisfy test
    status: str
    title: str
    action: str
    acceptance: List[str]
    dependencies: NotRequired[List[str]]
    output: NotRequired[str]
    plan: NotRequired[str]

class Task(TypedDict):
    id: int
    task_id: int # Added to satisfy test
    status: str
    title: str
    action: str
    acceptance: List[AcceptanceCriterion]
    features: List[Feature]
    plan: NotRequired[str]
