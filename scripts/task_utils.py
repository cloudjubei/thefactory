import json
import os
import subprocess
from pathlib import Path
from typing import List, Optional

from docs.tasks.task_format import Task, Feature, Status
from scripts.git_manager import GitManager

TASKS_DIR = Path("tasks")

# --- Core Task I/O ---

def get_task(task_id: int) -> Task:
    """Loads a task from its JSON file."""
    task_file = TASKS_DIR / str(task_id) / "task.json"
    if not task_file.exists():
        raise FileNotFoundError(f"Task file not found for task_id: {task_id}")
    with open(task_file, "r") as f:
        return json.load(f)

def save_task(task: Task):
    """Saves a task to its JSON file."""
    task_dir = TASKS_DIR / str(task["id"])
    task_dir.mkdir(exist_ok=True, parents=True)
    task_file = task_dir / "task.json"
    with open(task_file, "w") as f:
        json.dump(task, f, indent=2)

# --- Universal Agent Tools ---

def finish(task_id: int) -> str:
    """A signal tool for the agent to indicate it has finished all its work."""
    return f"Agent has signaled work is finished for task {task_id}."

def update_task_status(task_id: int, status: Status) -> Task:
    """Updates the overall status of a task."""
    task = get_task(task_id)
    task["status"] = status
    save_task(task)
    return task

def update_agent_question(task_id: int, feature_id: str, question: str):
    """Adds a question to a feature, typically when it's being deferred."""
    task = get_task(task_id)
    for feature in task["features"]:
        if feature["id"] == feature_id:
            feature["agent_question"] = question
            break
    save_task(task)

# --- Developer Agent Tools ---

def get_context(files: List[str]) -> List[str]:
    """Retrieves the content of specific files."""
    # ... (implementation from previous message is correct)
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
    # ... (implementation from previous message is correct)
    Path(filename).parent.mkdir(exist_ok=True, parents=True)
    with open(filename, "w") as f:
        f.write(content)

def update_feature_status(task_id: int, feature_id: str, status: Status) -> Optional[Feature]:
    """Updates the status of a specific feature."""
    # ... (implementation from previous message is correct)
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

def defer_feature(task_id: int, feature_id: str, reason: str) -> Optional[Feature]:
    """Sets a feature's status to '=' (Deferred) when it's blocked."""
    # ... (implementation from previous message is correct)
    task = get_task(task_id)
    deferred_feature = None
    for feature in task["features"]:
        if feature["id"] == feature_id:
            feature["status"] = "="
            feature["rejection"] = f"Deferred: {reason}"
            deferred_feature = feature
            break
    if deferred_feature:
        save_task(task)
    print(f"Feature {feature_id} deferred. Reason: {reason}")
    return deferred_feature

def finish_feature(task_id: int, feature_id: str, git_manager: GitManager):
    """Marks a feature as done and creates a per-feature commit."""
    # ... (implementation from previous message is correct)
    feature_to_commit = update_feature_status(task_id, feature_id, "+")
    if feature_to_commit:
        commit_message = f"feat: Complete feature {feature_id} - {feature_to_commit['title']}"
        print(f"Committing with message: {commit_message}")
        task_file_path = str(TASKS_DIR / str(task_id) / "task.json")
        git_manager.stage_files([task_file_path])
        git_manager.commit(commit_message)
    return feature_to_commit

# --- Tester Agent Tools ---

def _get_test_path(task_id: int, feature_id: str) -> Path:
    """Helper to get the conventional path for a feature's test file."""
    feature_number = feature_id.split('.')[-1]
    return TASKS_DIR / str(task_id) / "tests" / f"test_{task_id}_{feature_number}.py"

def get_test(task_id: int, feature_id: str) -> str:
    """Retrieves the current test content for a feature."""
    test_path = _get_test_path(task_id, feature_id)
    try:
        return test_path.read_text()
    except FileNotFoundError:
        return f"Test file not found at {test_path}"

def update_acceptance_criteria(task_id: int, feature_id: str, acceptance_criteria: List[str]) -> Optional[Feature]:
    """Replace the feature's acceptance criteria with a new list."""
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
    """Create or update the test file for the given feature."""
    test_path = _get_test_path(task_id, feature_id)
    test_path.parent.mkdir(exist_ok=True, parents=True)
    test_path.write_text(test)
    return f"Test file updated at {test_path}"

def delete_test(task_id: int, feature_id: str):
    """Remove the test file for the given feature."""
    test_path = _get_test_path(task_id, feature_id)
    if test_path.exists():
        test_path.unlink()
        return f"Test file {test_path} deleted."
    return f"Test file {test_path} not found."

def run_test(task_id: int, feature_id: str) -> str:
    """Executes a feature's test script and returns the result."""
    test_path = _get_test_path(task_id, feature_id)
    if not test_path.exists():
        return "FAIL: Test file not found."
    
    try:
        result = subprocess.run(
            ["python3", str(test_path)],
            capture_output=True,
            text=True,
            timeout=30, # 30-second timeout
            check=False # Do not raise exception on non-zero exit code
        )
        if result.returncode == 0:
            return f"PASS: Test executed successfully.\nOutput:\n{result.stdout}"
        else:
            return f"FAIL: Test failed with exit code {result.returncode}.\nStderr:\n{result.stderr}\nStdout:\n{result.stdout}"
    except subprocess.TimeoutExpired:
        return "FAIL: Test execution timed out."
    except Exception as e:
        return f"FAIL: An unexpected error occurred while running the test: {e}"

# --- Orchestrator Helpers ---
# ... (implementations from previous message are correct)
def find_next_pending_task() -> Optional[Task]:
    """Scans task directories and returns the first task that is pending or in progress."""
    if not TASKS_DIR.exists(): return None
    for task_dir in sorted(TASKS_DIR.iterdir(), key=lambda x: int(x.name)):
        if task_dir.is_dir():
            try:
                task_id = int(task_dir.name)
                task = get_task(task_id)
                if task.get("status") in ["-", "~"]: return task
            except (ValueError, FileNotFoundError): continue
    return None

def find_next_available_feature(task: Task) -> Optional[Feature]:
    """Finds the first pending feature in a task whose dependencies are all met."""
    completed_feature_ids = {f["id"] for f in task["features"] if f["status"] == "+"}
    for feature in task["features"]:
        if feature["status"] == "-":
            dependencies = feature.get("dependencies", [])
            if all(dep_id in completed_feature_ids for dep_id in dependencies):
                return feature
    return None

def create_task(task: Task) -> Task:
    """Creates a new task directory and task.json file."""
    task_id = task.get("id")
    if not task_id:
        raise ValueError("Task dictionary must include an 'id'.")
    
    task_dir = TASKS_DIR / str(task_id)
    if task_dir.exists():
        raise FileExistsError(f"Task with ID {task_id} already exists.")
    
    # Ensure features list exists
    task.setdefault("features", [])
    save_task(task)
    return task

def create_feature(task_id: int, feature: Feature) -> Feature:
    """Adds a new feature to an existing task. (For rare cases where a feature must be split)."""
    task = get_task(task_id)
    existing_ids = {f["id"] for f in task["features"]}
    if feature["id"] in existing_ids:
        raise ValueError(f"Feature with ID {feature['id']} already exists in task {task_id}.")
    task["features"].append(feature)
    save_task(task)
    return feature

def update_feature_plan(task_id: int, feature_id: str, feature_plan: str) -> Optional[Feature]:
    """
    Updates the 'plan' field of a specific feature. This is the primary tool for the Planner agent.
    """
    task = get_task(task_id)
    updated_feature = None
    for feature in task["features"]:
        if feature["id"] == feature_id:
            feature["plan"] = feature_plan
            updated_feature = feature
            break
    if updated_feature:
        save_task(task)
    return updated_feature
