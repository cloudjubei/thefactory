import os
import subprocess
import pytest

@pytest.fixture
def script_path():
    return 'scripts/run_local_agent.py'

def test_script_exists(script_path):
    assert os.path.exists(script_path), 'Orchestrator script does not exist'

def test_cli_options():
    result = subprocess.run(['python', 'scripts/run_local_agent.py', '--help'], capture_output=True, text=True)
    assert '--mode' in result.stdout
    assert '--task' in result.stdout
    assert '--agent' in result.stdout

def test_mode_options():
    # Test invalid mode
    result = subprocess.run(['python', 'scripts/run_local_agent.py', '--mode', 'invalid', '--task', '1', '--agent', 'planner'], capture_output=True, text=True)
    assert result.returncode != 0
    # Test valid modes
    # Note: Actual run might require mocking, but check parsing
    pass  # Expand with mocks if needed


# Additional tests for protocol compliance, imports, etc., would be added here.
# For example, check imports:
def test_imports():
    with open('scripts/run_local_agent.py', 'r') as f:
        content = f.read()
    assert 'from scripts.git_manager import GitManager' in content
    assert 'import scripts.tools_utils' in content or 'from scripts import tools_utils' in content
