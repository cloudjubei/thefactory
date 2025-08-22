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


# --- Developer Agent Tools ---

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

def block_feature(task_id: int, feature_id: str, reason: str) -> Optional[Feature]:
    """Sets a feature's status to '?' Blocked when it's blocked."""
    # ... (implementation from previous message is correct)
    task = get_task(task_id)
    deferred_feature = None
    for feature in task["features"]:
        if feature["id"] == feature_id:
            feature["status"] = "?"
            feature["rejection"] = f"Blocked: {reason}"
            deferred_feature = feature
            break
    if deferred_feature:
        save_task(task)
    print(f"Feature {feature_id} blocked. Reason: {reason}")
    return deferred_feature

def _check_and_update_task_completion(task_id: int):
    """Checks if all features in a task are done, and if so, marks the task as done."""
    task = get_task(task_id)
    all_features_done = all(f.get("status") == "+" for f in task["features"])
    
    if all_features_done:
        print(f"All features for task {task_id} are complete. Updating task status to '+'.")
        update_task_status(task_id, "+")

def finish_feature(task_id: int, feature_id: str, agent_type: str, git_manager: GitManager):
    """
    Handles the finishing logic for any agent. It stages all current changes,
    commits them, and updates the feature status according to the agent's role.
    """
    task = get_task(task_id)
    feature_title = ""
    for f in task['features']:
        if f['id'] == feature_id:
            feature_title = f['title']
            break

    # 1. Stage all unstaged changes in the repository.
    # This is a robust way to capture all work done by the agent in this turn.
    try:
        # Using GitManager to stage all changes. A simple '.' stages everything.
        git_manager.stage_files(['.'])
    except Exception as e:
        print(f"Warning: Could not stage files. Git error: {e}")
        # Continue anyway, as the status update is the most critical part.

    # 2. Define commit message and update status based on agent role.
    if agent_type == 'developer':
        commit_message = f"feat: Complete feature {feature_id} - {feature_title}"
        update_feature_status(task_id, feature_id, "+")
        # After a developer finishes, check if the whole task is done.
        _check_and_update_task_completion(task_id)
    elif agent_type == 'planner':
        commit_message = f"plan: Add plan for feature {feature_id} - {feature_title}"
        update_feature_status(task_id, feature_id, "-")
    elif agent_type == 'tester':
        commit_message = f"test: Add tests for feature {feature_id} - {feature_title}"
        update_feature_status(task_id, feature_id, "-")
    elif agent_type == 'contexter': 
        commit_message = f"context: Set context for feature {feature_id} - {feature_title}"
        update_feature_status(task_id, feature_id, "-")
    else:
        raise ValueError(f"Unknown agent_type '{agent_type}' called finish_feature.")

    # 3. Commit the staged changes.
    try:
        git_manager.commit(commit_message)
        print(f"Committed changes with message: '{commit_message}'")
    except Exception as e:
        print(f"Warning: Git commit failed. Error: {e}")
        
    return f"Feature {feature_id} finished by {agent_type} and changes committed."

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

def update_acceptance_criteria(task_id: int, feature_id: str, criteria: List[str]) -> Optional[Feature]:
    """Replace the feature's acceptance criteria with a new list."""
    task = get_task(task_id)
    updated_feature = None
    for feature in task["features"]:
        if feature["id"] == feature_id:
            feature["acceptance"] = criteria
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


def find_next_available_feature(task: Task, exclude_ids: set = set()) -> Optional[Feature]:
    """
    Finds the first pending feature in a task whose dependencies are all met,
    EXCLUDING any feature IDs passed in the `exclude_ids` set.
    """

    completed_feature_ids = {f["id"] for f in task["features"] if f["status"] == "+"}
    
    for feature in task["features"]:
        if feature["id"] in exclude_ids:
            continue
        if feature["status"] == "-":
            dependencies = feature.get("dependencies", [])
            if all(dep_id in completed_feature_ids for dep_id in dependencies):
                return feature
    return None

def create_feature(task_id: int, feature: Feature) -> Feature:
    """Adds a new feature to an existing task. (For rare cases where a feature must be split)."""
    task = get_task(task_id)
    existing_ids = {f["id"] for f in task["features"]}
    if feature["id"] in existing_ids:
        raise ValueError(f"Feature with ID {feature['id']} already exists in task {task_id}.")
    task["features"].append(feature)
    save_task(task)
    return feature

def update_feature_plan(task_id: int, feature_id: str, plan: any) -> Optional[Feature]:
    """
    Updates the 'plan' field of a specific feature. This is the primary tool for the Planner agent.
    It gracefully handles the plan being passed as a list of strings.
    """
    plan_str = ""

    if isinstance(plan, list):
        plan_str = "\n".join(map(str, plan))
    elif isinstance(plan, str):
        plan_str = plan
    else:
        print(f"Warning: Plan received with unexpected type '{type(plan)}'. Converting to string.")
        plan_str = str(plan)

    task = get_task(task_id)
    updated_feature = None
    for feature in task["features"]:
        if feature["id"] == feature_id:
            feature["plan"] = plan_str
            updated_feature = feature
            break
    if updated_feature:
        save_task(task)
    return updated_feature

def update_feature_context(task_id: int, feature_id: str, context: List[str]) -> Optional[Feature]:
    """
    Updates the 'context' field of a specific feature. This is the primary tool for the Contexter agent.
    """
    task = get_task(task_id)
    updated_feature = None
    for feature in task["features"]:
        if feature["id"] == feature_id:
            feature["context"] = context
            updated_feature = feature
            break
    if updated_feature:
        save_task(task)
    return updated_feature