import os
import subprocess
import importlib.util
import sys

def test_orchestrator_script():
    script_path = 'scripts/run_local_agent.py'
    assert os.path.exists(script_path), 'Script file does not exist'

    # Check CLI options via --help
    try:
        result = subprocess.run(['python', script_path, '--help'], capture_output=True, text=True, check=True)
        help_text = result.stdout
    except subprocess.CalledProcessError:
        assert False, 'Script fails to run with --help'
    assert '--mode' in help_text, 'Missing --mode option'
    assert '--task' in help_text, 'Missing --task option'
    assert '--feature' in help_text, 'Missing --feature option'
    assert '--agent' in help_text, 'Missing --agent option'

    # Check for specific imports in file content
    with open(script_path, 'r') as f:
        content = f.read()
    assert 'git_manager' in content and 'GitManager' in content, 'Missing reference to GitManager from scripts/git_manager.py'
    assert 'tools_utils' in content, 'Missing reference to scripts/tools_utils.py'

    # Load the module to check for functions
    spec = importlib.util.spec_from_file_location('orchestrator', script_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules['orchestrator'] = module
    spec.loader.exec_module(module)

    # Check for context and tools functions (assuming possible names based on description)
    context_func_names = ['gather_context', 'get_context', 'get_context_for_agent', 'gather_agent_context']
    tools_func_names = ['gather_tools', 'get_tools', 'get_tools_for_agent', 'gather_agent_tools']
    assert any(hasattr(module, name) for name in context_func_names), 'Missing function to gather context'
    assert any(hasattr(module, name) for name in tools_func_names), 'Missing function to gather tools'

    # Note: Criteria related to protocol compliance, data passing, and conversation flow require functional/integration tests with mocks (e.g., mock LLM responses to test loops and tool calls). These can be added post-implementation.

test_orchestrator_script()