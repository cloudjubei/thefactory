import json
from pathlib import Path
from typing import List, Optional

from docs.tasks.task_format import Task, Feature, Status
from scripts.git_manager import GitManager

TASKS_DIR = Path("tasks")

def get_task(task_id: int) -> Task:
    """Loads a task from its JSON file."""
    task_file = TASKS_DIR / str(task_id) / "task.json"
    with open(task_file, "r") as f:
        return json.load(f)

def save_task(task: Task):
    """Saves a task to its JSON file."""
    task_dir = TASKS_DIR / str(task["id"])
    task_dir.mkdir(exist_ok=True)
    task_file = task_dir / "task.json"
    with open(task_file, "w") as f:
        json.dump(task, f, indent=2)

# Developer Tools
def get_context(files: List[str]) -> List[str]:
    """Retrieves the content of specific files."""
    content = []
    for file_path in files:
        try:
            with open(file_path, "r") as f:
                content.append(f.read())
        except FileNotFoundError:
            content.append(f"File not found: {file_path}")
    return content

def write_file(filename: str, content: str):
    """Creates or overwrites a file with the full content."""
    with open(filename, "w") as f:
        f.write(content)

def run_test(task_id: int, feature_id: str) -> str:
    """A placeholder for running a feature's test."""
    # In a real implementation, this would execute the test file.
    return f"Test for task {task_id}, feature {feature_id} would be run here."

def finish_feature(task_id: int, feature_id: str, git_manager: GitManager):
    """Marks a feature as done and creates a per-feature commit."""
    task = get_task(task_id)
    feature_to_commit = None
    for feature in task["features"]:
        if feature["id"] == feature_id:
            feature["status"] = "+"
            feature_to_commit = feature
            break
    if feature_to_commit:
        save_task(task)
        commit_message = f"feat: Implement feature {feature_id} - {feature_to_commit['title']}"
        # In a real scenario, you'd determine which files were changed for this feature.
        # For this example, we'll assume the task file is what's being committed.
        git_manager.stage_files([str(TASKS_DIR / str(task_id) / "task.json")])
        git_manager.commit(commit_message)
    return feature_to_commit

# Planner and Tester Tools
def update_task_status(task_id: int, status: Status) -> Task:
    """Updates the overall status of a task."""
    task = get_task(task_id)
    task["status"] = status
    save_task(task)
    return task

def update_feature_status(task_id: int, feature_id: str, status: Status) -> Optional[Feature]:
    """Updates the status of a specific feature."""
    task = get_task(task_id)
    updated_feature = None
    for feature in task["features"]:
        if feature["id"] == feature_id:
            feature["status"] = status
            updated_feature = feature
            break
    if updated_feature:
        save_task(task)
    return updated_feature

def update_agent_question(task_id: int, question: str, feature_id: Optional[str] = None):
    """Adds a question to a task or feature."""
    task = get_task(task_id)
    if feature_id:
        for feature in task["features"]:
            if feature["id"] == feature_id:
                feature["agent_question"] = question
                break
    else:
        task["agent_question"] = question
    save_task(task)

# Tester Tools
def update_acceptance_criteria(task_id: int, feature_id: str, acceptance_criteria: List[str]) -> Optional[Feature]:
    """Updates the acceptance criteria for a feature."""
    task = get_task(task_id)
    updated_feature = None
    for feature in task["features"]:
        if feature["id"] == feature_id:
            feature["acceptance"] = acceptance_criteria
            updated_feature = feature
            break
    if updated_feature:
        save_task(task)
    return updated_feature

def update_test(task_id: int, feature_id: str, test: str):
    """Creates or updates the test for a given feature."""
    test_dir = TASKS_DIR / str(task_id) / "tests"
    test_dir.mkdir(exist_ok=True)
    feature_number = feature_id.split('.')[-1]
    test_file = test_dir / f"test_{task_id}_{feature_number}.py"
    with open(test_file, "w") as f:
        f.write(test)