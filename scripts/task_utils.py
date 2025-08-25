import json
import os
import subprocess
from pathlib import Path
from typing import List, Optional

from docs.tasks.task_format import Task, Feature, Status
from scripts.git_manager import GitManager

# Project root can be dynamically set by the orchestrator to target a child project.
_PROJECT_ROOT = Path.cwd()


def set_project_root(path: str | Path) -> None:
    """Set the active project root used by task utilities (tasks/, tests/, writes, etc.)."""
    global _PROJECT_ROOT
    _PROJECT_ROOT = Path(path).resolve()


def get_project_root() -> Path:
    return _PROJECT_ROOT


TASKS_DIR_NAME = "tasks" 


def _get_tasks_dir() -> Path:
    return _PROJECT_ROOT / TASKS_DIR_NAME

def _get_task_dir(task_id: int) -> Path:
    return _get_tasks_dir() / str(task_id)

def _get_task_path(task_id: int) -> Path:
    return _get_task_dir(task_id) / "task.json"

def _get_test_path(task_id: int, feature_id: str) -> Path:
    """Helper to get the conventional path for a feature's test file."""
    feature_number = feature_id.split('.')[-1]
    return _get_task_dir(task_id) / "tests" / f"test_{task_id}_{feature_number}.py"

# --- Core Task I/O ---

def get_task(task_id: int) -> Task:
    task_file = _get_task_path(task_id)
    if not task_file.exists():
        raise FileNotFoundError(f"Task file not found for task_id: {task_id}")
    with open(task_file, "r") as f:
        return json.load(f)


def save_task(task: Task):
    """Saves a task to its JSON file."""
    task_file = _get_task_path(task.get('id'))
    task_file.parent.mkdir(parents=True, exist_ok=True)
    with open(task_file, "w") as f:
        json.dump(task, f, indent=2)


def update_task_status(task_id: int, status: Status) -> Task:
    """Updates the overall status of a task."""
    task = get_task(task_id)
    task["status"] = status
    save_task(task)
    return task

# --- Developer Agent Tools ---

def get_context(files: List[str]) -> str:
    """
    Retrieves the content of specified paths relative to the current PROJECT ROOT.
    - If a path is a file, its content is returned.
    - If a path is a directory, the names of the files within it are returned as a JSON array string.
    - Paths outside of the project root are blocked for safety.
    """
    content = {}
    for file_path_str in files:
        target_path = (get_project_root() / file_path_str).resolve()
        try:
            # Ensure access stays within project root
            target_path.relative_to(get_project_root())

            if target_path.is_dir():
                dir_files = [f.name for f in target_path.iterdir()]
                content[file_path_str] = dir_files
            elif target_path.is_file():
                content[file_path_str] = target_path.read_text()
            else:
                content[file_path_str] = "Path not found or is not a regular file/directory."

        except (ValueError, PermissionError):
            content[file_path_str] = "SECURITY ERROR: Cannot access path outside project directory.\n"
        except FileNotFoundError:
            content[file_path_str] = "Path not found or is not a regular file/directory."
        
    return json.dumps(content, indent=0)


def write_file(filename: str, content: str):
    """Creates or overwrites a file, ensuring it's safely within the given project root."""
    target_file_path = (get_project_root() / filename).resolve()
    try:
        target_file_path.relative_to(get_project_root())
    except ValueError:
        raise PermissionError(f"Security violation: Attempted to write outside of project root: {filename}")
    
    target_file_path.parent.mkdir(exist_ok=True, parents=True)
    target_file_path.write_text(content)
    print(f"File securely written to: {filename}")


def update_feature_status(task_id: int, feature_id: str, status: Status) -> Optional[Feature]:
    """Updates the status of a specific feature."""
    task = get_task(task_id)
    updated_feature = None
    for feature in task.get("features"):
        if feature.get("id") == feature_id:
            feature["status"] = status
            updated_feature = feature
            break
    if updated_feature:
        save_task(task)
    return updated_feature


def block_feature(task_id: int, feature_id: str, reason: str, agent_type: str, git_manager: GitManager) -> Optional[Feature]:
    """Sets a feature's status to '?' Blocked when it's blocked."""
    task = get_task(task_id)
    deferred_feature = None
    for feature in task.get("features"):
        if feature.get("id") == feature_id:
            feature["status"] = "?"
            feature["rejection"] = f"Blocked: {reason}"
            feature_title = feature.get('title', '')
            deferred_feature = feature
            break
    feature_title = ""
    if deferred_feature:
        save_task(task)

    if agent_type == 'developer':
        commit_message = f"BLOCKED feat: Complete feature {feature_id} - {feature_title}"
    elif agent_type == 'planner':
        commit_message = f"BLOCKED plan: Add plan for feature {feature_id} - {feature_title}"
    elif agent_type == 'tester':
        commit_message = f"BLOCKED test: Add tests for feature {feature_id} - {feature_title}"
    elif agent_type == 'contexter': 
        commit_message = f"BLOCKED context: Set context for feature {feature_id} - {feature_title}"
    else:
        raise ValueError(f"Unknown agent_type '{agent_type}' called block_feature.")
    try:
        git_manager.stage_files(['.'])
    except Exception as e:
        print(f"Warning: Could not stage files. Git error: {e}")
    try:
        git_manager.commit(commit_message)
        print(f"Committed changes with message: '{commit_message}'")
    except Exception as e:
        print(f"Warning: Git commit failed. Error: {e}")
    try:
        git_manager.push()
    except Exception as e:
        print(f"Could not push': {e}")

    print(f"Feature {feature_id} blocked. Reason: {reason}")
    return deferred_feature


def block_task(task_id: int, reason: str) -> Task:
    """Sets a task's status to '?' Blocked when it's blocked."""
    task = get_task(task_id)
    
    task["status"] = "?"
    task["rejection"] = f"Blocked: {reason}"
    save_task(task)

    print(f"Task {task_id} blocked. Reason: {reason}")
    return task


def _check_and_update_task_completion(task_id: int):
    """Checks if all features in a task are done, and if so, marks the task as done."""
    task = get_task(task_id)
    all_features_done = all(f.get("status") == "+" for f in task.get("features"))
    
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
    for f in task.get('features'):
        if f.get('id') == feature_id:
            feature_title = f.get('title')
            break

    if agent_type == 'developer':
        commit_message = f"feat: Complete feature {feature_id} - {feature_title}"
        update_feature_status(task_id, feature_id, "+")
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

    try:
        git_manager.stage_files(['.'])
    except Exception as e:
        print(f"Warning: Could not stage files. Git error: {e}")
    try:
        git_manager.commit(commit_message)
        print(f"Committed changes with message: '{commit_message}'")
    except Exception as e:
        print(f"Warning: Git commit failed. Error: {e}")
    try:
        git_manager.push()
    except Exception as e:
        print(f"Could not push': {e}")
        
    return f"Feature {feature_id} finished by {agent_type} and changes committed."


def finish_spec(task_id: int, agent_type: str, git_manager: GitManager):
    """
    Handles the finishing logic for any agent. It stages all current changes.
    """
    try:
        git_manager.stage_files(['.'])
    except Exception as e:
        print(f"Warning: Could not stage files. Git error: {e}")

    if agent_type == 'speccer':
        commit_message = f"spec: Added spec for task: {task_id}"
    else:
        raise ValueError(f"Unknown agent_type '{agent_type}' called finish_spec.")

    try:
        git_manager.commit(commit_message)
        print(f"Committed changes with message: '{commit_message}'")
    except Exception as e:
        print(f"Warning: Git commit failed. Error: {e}")
        
    return f"Task {task_id} finished spec by {agent_type} and changes committed."

# --- Tester Agent Tools ---


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
    for feature in task.get("features"):
        if feature.get("id") == feature_id:
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
        print(f"Running test at {test_path}")
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

def find_next_pending_task() -> Optional[Task]:
    """Scans task directories and returns the first task that is pending or in progress."""
    if not _get_tasks_dir().exists(): return None
    for task_dir in sorted(_get_tasks_dir().iterdir(), key=lambda x: int(x.name)):
        if task_dir.is_dir():
            try:
                task_id = int(task_dir.name)
                task = get_task(task_id)
                if task.get("status") in ["-", "~"]: return task
            except (ValueError, FileNotFoundError): continue
    return None


def find_next_available_feature(task: Task, exclude_ids: set = set(), ignore_depedencies: bool = False) -> Optional[Feature]:
    """
    Finds the first pending feature in a task whose dependencies are all met,
    EXCLUDING any feature IDs passed in the `exclude_ids` set.
    """

    completed_feature_ids = {f.get("id") for f in task.get("features") if f.get("status") == "+"}
    
    for feature in task["features"]:
        if feature.get("id") in exclude_ids:
            continue
        if feature.get("status") == "-":
            dependencies = feature.get("dependencies", [])
            if ignore_depedencies or all(dep_id in completed_feature_ids for dep_id in dependencies):
                return feature
    return None


def create_feature(task_id: int, title: str, description: str) -> Feature:
    """
    Creates a new feature with a given title, description, and adds it to the specified task.
    This tool automatically generates a new feature ID.
    """
    task = get_task(task_id)
    features = task.get("features", [])
    
    highest_sub_id = 0
    for f in features:
        try:
            sub_id = int(f['id'].split('.')[-1])
            if sub_id > highest_sub_id:
                highest_sub_id = sub_id
        except (ValueError, IndexError):
            continue
    
    new_sub_id = highest_sub_id + 1
    new_id = f"{task_id}.{new_sub_id}"

    new_feature: Feature = {
        "id": new_id,
        "status": "-",
        "title": title,
        "description": description,
        "plan": "",
        "context": [],
        "acceptance": [],
    }
    
    features.append(new_feature)
    task["features"] = features
    save_task(task)
    
    print(f"New feature '{new_id}' created in task {task_id}.")
    return new_feature


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
    for feature in task.get("features"):
        if feature.get("id") == feature_id:
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
    for feature in task.get("features"):
        if feature.get("id") == feature_id:
            feature["context"] = context
            updated_feature = feature
            break
    if updated_feature:
        save_task(task)
    return updated_feature
