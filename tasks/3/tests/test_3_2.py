import unittest
import subprocess
import os
import tempfile
import shutil
import sys
from pathlib import Path
import re

class TestChildProjectUtils(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.parent_path = Path(self.temp_dir.name)
        # Copy the script from actual repo to temp dir
        script_source = Path(__file__).resolve().parent.parent.parent.parent / 'scripts' / 'child_project_utils.py'
        scripts_dir = self.parent_path / 'scripts'
        scripts_dir.mkdir(exist_ok=True)
        self.script_path = scripts_dir / 'child_project_utils.py'
        shutil.copy(script_source, self.script_path)
        self.script_path.chmod(0o755)  # Make executable
        # Initialize parent as git repo
        subprocess.run(['git', 'init'], cwd=self.parent_path, check=True, capture_output=True)

    def tearDown(self):
        self.temp_dir.cleanup()

    def run_script(self, args, check=True):
        cmd = [sys.executable, str(self.script_path)] + args
        result = subprocess.run(cmd, cwd=self.parent_path, capture_output=True, text=True)
        if check:
            self.assertEqual(result.returncode, 0, f'Script failed: {result.stderr}')
        return result

    def test_cli_entry_point_and_help(self):
        # Criterion 1 and 10: CLI exists, accepts args, has help
        result = self.run_script(['--help'], check=False)
        self.assertEqual(result.returncode, 0)
        self.assertIn('usage:', result.stdout)
        self.assertIn('project_name', result.stdout)
        self.assertIn('--description', result.stdout)
        self.assertIn('--repo-url', result.stdout)
        self.assertIn('--path', result.stdout)
        self.assertIn('--dry-run', result.stdout)
        self.assertIn('Examples:', result.stdout)

    def test_create_new_project(self):
        # Criterion 2,3,4,6,9: Create dir, structure, git init, submodule, exit 0
        project_name = 'test_project'
        description = 'Test description'
        result = self.run_script([project_name, '--description', description])
        self.assertEqual(result.returncode, 0)

        project_path = self.parent_path / 'projects' / project_name
        self.assertTrue(project_path.exists())
        self.assertTrue((project_path / 'README.md').exists())
        with open(project_path / 'README.md') as f:
            content = f.read()
            self.assertIn(f'# {project_name}', content)
            self.assertIn(description, content)
        self.assertTrue((project_path / '.gitignore').exists())
        self.assertTrue((project_path / 'tasks' / '000_initial_task.md').exists())
        with open(project_path / 'tasks' / '000_initial_task.md') as f:
            self.assertIn('Initial Task', f.read())

        # Git init in child
        git_dir = project_path / '.git'
        self.assertTrue(git_dir.exists())
        status = subprocess.run(['git', 'status'], cwd=project_path, capture_output=True, text=True)
        self.assertEqual(status.returncode, 0)
        self.assertIn('nothing to commit', status.stdout)

        # Submodule in parent
        gitmodules = self.parent_path / '.gitmodules'
        self.assertTrue(gitmodules.exists())
        with open(gitmodules) as f:
            content = f.read()
            self.assertIn(f'path = projects/{project_name}', content)
            self.assertIn(f'url = ./projects/{project_name}', content)

    def test_repo_url(self):
        # Criterion 5: Sets origin if repo_url provided
        project_name = 'test_project_url'
        repo_url = 'git@example.com:test/repo.git'
        self.run_script([project_name, '--repo-url', repo_url])
        project_path = self.parent_path / 'projects' / project_name
        remote = subprocess.run(['git', 'remote', 'get-url', 'origin'], cwd=project_path, capture_output=True, text=True)
        self.assertEqual(remote.returncode, 0)
        self.assertIn(repo_url, remote.stdout)

        # Check .gitmodules uses the provided url
        with open(self.parent_path / '.gitmodules') as f:
            content = f.read()
            self.assertIn(f'url = {repo_url}', content)

    def test_existing_directory_error(self):
        # Criterion 2,7,9: Errors if exists, idempotent, non-zero exit, message
        project_name = 'existing_project'
        project_path = self.parent_path / 'projects' / project_name
        project_path.mkdir(parents=True)
        result = self.run_script([project_name], check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('already exists', result.stderr)

        # Rerun should fail similarly without changes
        result2 = self.run_script([project_name], check=False)
        self.assertNotEqual(result2.returncode, 0)
        self.assertIn('already exists', result2.stderr)

    def test_dry_run(self):
        # Criterion 8: Prints plans, no changes
        project_name = 'dry_project'
        result = self.run_script([project_name, '--dry-run'], check=False)
        self.assertEqual(result.returncode, 0)  # Dry run succeeds
        self.assertIn('DRY RUN', result.stdout)
        self.assertIn('Planning filesystem changes', result.stdout)
        self.assertIn('Planning child git repository initialization', result.stdout)
        self.assertIn('Planning submodule addition', result.stdout)

        project_path = self.parent_path / 'projects' / project_name
        self.assertFalse(project_path.exists())  # No changes made
        self.assertFalse((self.parent_path / '.gitmodules').exists())

if __name__ == '__main__':
    unittest.main()