import types
from pathlib import Path

import importlib


def test_project_root_is_cwd():
    # Import locally to ensure PROJECT_ROOT is set based on current cwd at import time
    from scripts import run_local_agent as rla
    assert rla.PROJECT_ROOT == Path.cwd()


def test_orchestrator_scoped_to_child_directory(monkeypatch):
    from scripts import run_local_agent as rla

    # Simulate running within a child project directory by overriding PROJECT_ROOT
    fake_child_root = Path.cwd() / "fake_child_project"
    monkeypatch.setattr(rla, "PROJECT_ROOT", fake_child_root)

    # Track calls to GitManager
    class DummyGitManager:
        last_instance = None
        def __init__(self, path):
            self.path = path
            self.checkout_calls = []
            self.pull_calls = []
            self.push_calls = []
            DummyGitManager.last_instance = self
        def checkout_branch(self, name):
            self.checkout_calls.append(name)
        def pull(self, name):
            self.pull_calls.append(name)
        def push(self, name):
            self.push_calls.append(name)

    monkeypatch.setattr(rla, "GitManager", DummyGitManager)

    # Fake task pipeline
    dummy_task = {"id": 42, "title": "Dummy Child Task", "description": ""}

    monkeypatch.setattr(rla.task_utils, "find_next_pending_task", lambda: dummy_task)
    monkeypatch.setattr(rla.task_utils, "get_task", lambda task_id: dummy_task)

    # Avoid real agent execution and LLM calls
    agent_called = {"called": False}
    def fake_run_agent_on_task(model, agent_type, task, git_manager):
        agent_called["called"] = True
        return True
    monkeypatch.setattr(rla, "run_agent_on_task", fake_run_agent_on_task)

    # Run orchestrator as speccer to ensure it proceeds into agent stage
    rla.run_orchestrator(model="test-model", agent_type="speccer", task_id=None)

    # Validate GitManager was instantiated with the child directory path
    gm = DummyGitManager.last_instance
    assert gm is not None
    assert gm.path == str(fake_child_root)

    # Validate branch operations on features/<task_id>
    expected_branch = f"features/{dummy_task['id']}"
    assert gm.checkout_calls == [expected_branch]
    assert gm.pull_calls == [expected_branch]
    assert gm.push_calls == [expected_branch]

    # Ensure agent stage was invoked without path errors
    assert agent_called["called"] is True


def test_orchestrator_root_repo_compatibility(monkeypatch):
    from scripts import run_local_agent as rla

    # Ensure running from repository root still works
    monkeypatch.setattr(rla, "PROJECT_ROOT", Path.cwd())

    class DummyGitManager:
        last_instance = None
        def __init__(self, path):
            self.path = path
            self.checkout_calls = []
            self.pull_calls = []
            self.push_calls = []
            DummyGitManager.last_instance = self
        def checkout_branch(self, name):
            self.checkout_calls.append(name)
        def pull(self, name):
            self.pull_calls.append(name)
        def push(self, name):
            self.push_calls.append(name)

    monkeypatch.setattr(rla, "GitManager", DummyGitManager)

    # Provide a specific task ID and task data
    given_task_id = 7
    dummy_task = {"id": given_task_id, "title": "Root Task", "description": ""}

    monkeypatch.setattr(rla.task_utils, "get_task", lambda task_id: dummy_task)

    agent_called = {"called": False}
    def fake_run_agent_on_task(model, agent_type, task, git_manager):
        agent_called["called"] = True
        return True
    monkeypatch.setattr(rla, "run_agent_on_task", fake_run_agent_on_task)

    rla.run_orchestrator(model="test-model", agent_type="speccer", task_id=given_task_id)

    gm = DummyGitManager.last_instance
    assert gm is not None
    # Should be scoped to the root directory (cwd)
    assert gm.path == str(Path.cwd())

    expected_branch = f"features/{given_task_id}"
    assert gm.checkout_calls == [expected_branch]
    assert gm.pull_calls == [expected_branch]
    assert gm.push_calls == [expected_branch]
    assert agent_called["called"] is True
