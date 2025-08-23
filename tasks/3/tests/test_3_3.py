import os
import sys
import shutil
import importlib
from pathlib import Path

IGNORE_PATTERNS = shutil.ignore_patterns('venv', '__pycache__', '*.pyc', '.idea', '.git')

class StubGitManager:
    instances = []
    def __init__(self, root_path: str):
        self.root_path = root_path
        self.calls = []
        StubGitManager.instances.append(self)
    def checkout_branch(self, name: str):
        self.calls.append(("checkout_branch", name))
    def pull(self, name: str):
        self.calls.append(("pull", name))
    def push(self, name: str):
        self.calls.append(("push", name))

DUMMY_TASK = {"id": 123, "title": "Dummy", "description": "Dummy task for orchestrator scope test"}


def copy_repo(src: Path, dst: Path):
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=IGNORE_PATTERNS)


def load_orchestrator_module_from(workspace: Path):
    # Ensure fresh import from the workspace copy
    sys.path.insert(0, str(workspace))
    for mod in [
        'scripts.run_local_agent',
        'scripts.task_utils',
        'scripts.git_manager',
        'docs.tasks.task_format'
    ]:
        if mod in sys.modules:
            del sys.modules[mod]
    try:
        mod = importlib.import_module('scripts.run_local_agent')
        return mod
    finally:
        # Keep workspace on sys.path during test execution of this module
        pass


def setup_orchestrator_stubs(rla):
    # Patch GitManager with stub
    rla.GitManager = StubGitManager
    # Stub task discovery to supply a dummy task and avoid filesystem dependency
    rla.task_utils.find_next_pending_task = lambda: DUMMY_TASK
    rla.task_utils.get_task = lambda task_id: DUMMY_TASK
    # Avoid reading real context files and agent work
    rla.task_utils.get_context = lambda files: ["<stubbed context>"]
    rla.run_agent_on_task = lambda model, agent_type, task, git_manager: True
    rla.run_agent_on_feature = lambda model, agent_type, task, feature, git_manager: True


def assert_git_calls_for_task():
    assert StubGitManager.instances, "GitManager was not instantiated"
    gm = StubGitManager.instances[-1]
    # Expect checkout, pull, then push on features/<task_id>
    expected_branch = f"features/{DUMMY_TASK['id']}"
    # The first two calls must be checkout and pull; push occurs at the end
    assert gm.calls[0] == ("checkout_branch", expected_branch)
    assert gm.calls[1] == ("pull", expected_branch)
    assert gm.calls[-1] == ("push", expected_branch)


def test_orchestrator_scopes_to_repo_root(tmp_path):
    # Arrange: copy repo to workspace
    repo_root = Path(__file__).resolve().parents[3]
    workspace = tmp_path / 'workspace'
    copy_repo(repo_root, workspace)

    # Act: run orchestrator from workspace root
    cwd_before = Path.cwd()
    try:
        os.chdir(workspace)
        rla = load_orchestrator_module_from(workspace)
        setup_orchestrator_stubs(rla)
        # Run orchestrator in speccer mode so it uses run_agent_on_task path
        rla.run_orchestrator(model='test-model', agent_type='speccer', task_id=None)
    finally:
        os.chdir(cwd_before)

    # Assert: GitManager root is the repo root workspace, and branch ops were called
    gm = StubGitManager.instances[-1]
    assert Path(gm.root_path) == workspace
    assert_git_calls_for_task()


def test_orchestrator_scopes_to_child_directory(tmp_path):
    # Arrange: copy repo to workspace and create child project directory
    repo_root = Path(__file__).resolve().parents[3]
    workspace = tmp_path / 'workspace'
    copy_repo(repo_root, workspace)
    child_dir = workspace / 'projects' / 'child-a'
    child_dir.mkdir(parents=True, exist_ok=True)

    # Act: run orchestrator from child directory
    cwd_before = Path.cwd()
    try:
        os.chdir(child_dir)
        rla = load_orchestrator_module_from(workspace)
        setup_orchestrator_stubs(rla)
        rla.run_orchestrator(model='test-model', agent_type='speccer', task_id=None)
    finally:
        os.chdir(cwd_before)

    # Assert: GitManager root is the child directory, and branch ops were called
    gm = StubGitManager.instances[-1]
    assert Path(gm.root_path) == child_dir
    assert_git_calls_for_task()
