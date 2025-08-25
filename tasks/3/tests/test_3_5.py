import sys
from pathlib import Path
import tempfile
from unittest.mock import patch
sys.path.insert(0, 'scripts')
import child_project_utils as cpu

original_run_command = cpu.run_command

def mock_run_command(command, cwd=None, dry_run=False, allow_fail=False):
    command_str = ' '.join(map(str, command))
    if 'git submodule add' in command_str:
        print('Skipping git submodule add for test')
        return None
    elif 'git' in command_str:
        print(f'Skipping git command for test: {command_str}')
        return None
    else:
        return original_run_command(command, cwd, dry_run, allow_fail)

with tempfile.TemporaryDirectory() as tmpdir:
    tmp_path = Path(tmpdir)
    original_argv = sys.argv
    sys.argv = ['child_project_utils.py', 'test_child', '-d', 'Test', '-p', str(tmp_path), '--dry-run']
    with patch('child_project_utils.run_command', mock_run_command):
        with patch('child_project_utils.check_git_installed', lambda: None):
            cpu.main()
    sys.argv = original_argv
    project_path = tmp_path / 'test_child'
    assert (project_path / 'src').is_dir(), '1. src/ not created'
    assert (project_path / 'docs').is_dir(), '2. docs/ not created'
    fo_path = project_path / 'docs' / 'FILE_ORGANISATION.md'
    assert fo_path.is_file(), '3. FILE_ORGANISATION.md not created'
    content = fo_path.read_text(encoding='utf-8')
    required_items = ['src/', 'docs/', 'tasks/', '.env', '.gitignore', 'README.md', 'File Naming Conventions', 'Evolution Guidance']
    for item in required_items:
        assert item in content, f'4. {item} not in child FILE_ORGANISATION.md'
    script_code = Path('scripts/child_project_utils.py').read_text(encoding='utf-8')
    required_actions = ['Create directory: src', 'Create directory: docs', 'Create file: docs/FILE_ORGANISATION.md']
    for action in required_actions:
        assert action in script_code, f'5. {action} not in plan_actions'
    parent_content = Path('docs/FILE_ORGANISATION.md').read_text(encoding='utf-8')
    assert '## Child Project Structure' in parent_content, '6. Missing child project structure section in parent doc'
    assert 'src/' in parent_content, '7. Example tree does not reflect child structure (missing src/)' 
print('All tests passed')