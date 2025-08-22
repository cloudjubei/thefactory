import unittest
import subprocess
import sys
import os
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, call

# Add scripts directory to path to allow import
sys.path.append(str(Path(__file__).parent.parent.parent.parent / 'scripts'))

import child_project_utils

class TestChildProjectUtils(unittest.TestCase):

    def setUp(self):
        """Set up a temporary directory and initialize a git repo in it."""
        self.test_dir = Path(tempfile.mkdtemp())
        self.original_cwd = Path.cwd()
        os.chdir(self.test_dir)
        subprocess.run(["git", "init"], check=True, capture_output=True)

    def tearDown(self):
        """Clean up the temporary directory."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    @patch('sys.stdout')
    @patch('sys.stderr')
    def test_help_message(self, mock_stderr, mock_stdout):
        """Test that -h/--help shows a help message and exits cleanly."""
        with self.assertRaises(SystemExit) as cm:
            sys.argv = ['child_project_utils.py', '--help']
            child_project_utils.main()
        self.assertEqual(cm.exception.code, 0)
        written_output = "".join(c.args[0] for c in mock_stdout.write.call_args_list)
        self.assertIn("usage: child_project_utils.py", written_output)
        self.assertIn("Examples:", written_output)

    @patch('child_project_utils.run_command')
    def test_dry_run(self, mock_run_command):
        """Test --dry-run prints actions but makes no changes."""
        project_name = "dry-run-project"
        projects_path_str = "projects"
        project_path = Path(projects_path_str) / project_name

        sys.argv = [
            'child_project_utils.py',
            project_name,
            '--description', 'A test project.',
            '--path', projects_path_str,
            '--dry-run'
        ]

        with self.assertRaises(SystemExit) as cm:
            child_project_utils.main()
        self.assertEqual(cm.exception.code, 0)

        self.assertFalse((self.test_dir / project_path).exists())

        expected_calls = [
            call(['git', 'init'], cwd=project_path, dry_run=True),
            call(['git', 'add', '.'], cwd=project_path, dry_run=True),
            call(['git', 'commit', '-m', 'Initial commit from scaffolding script'], cwd=project_path, dry_run=True),
            call(['git', 'submodule', 'add', f'./{project_path}', str(project_path)], dry_run=True)
        ]
        mock_run_command.assert_has_calls(expected_calls)

    @patch('subprocess.run')
    def test_project_creation_local(self, mock_subprocess_run):
        """Test successful creation of a project with a local submodule path."""
        project_name = "local-project"
        projects_path_str = "projects"
        # This is the path the script will work with internally (relative)
        relative_project_path = Path(projects_path_str) / project_name
        # This is the actual path on disk for setup/verification (absolute)
        absolute_project_path = self.test_dir / relative_project_path

        mock_subprocess_run.return_value = subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr="")

        sys.argv = [
            'child_project_utils.py',
            project_name,
            '--path', projects_path_str
        ]

        with self.assertRaises(SystemExit) as cm:
            child_project_utils.main()
        self.assertEqual(cm.exception.code, 0)

        self.assertTrue(absolute_project_path.exists())

        expected_calls = [
            call(['git', '--version'], check=True, capture_output=True),
            call(['git', 'init'], cwd=relative_project_path, check=True, capture_output=True, text=True, encoding='utf-8'),
            call(['git', 'add', '.'], cwd=relative_project_path, check=True, capture_output=True, text=True, encoding='utf-8'),
            call(['git', 'commit', '-m', 'Initial commit from scaffolding script'], cwd=relative_project_path, check=True, capture_output=True, text=True, encoding='utf-8'),
            call(['git', 'submodule', 'add', f'./{relative_project_path}', str(relative_project_path)], cwd=None, check=True, capture_output=True, text=True, encoding='utf-8')
        ]
        mock_subprocess_run.assert_has_calls(expected_calls, any_order=False)

    @patch('subprocess.run')
    def test_project_creation_with_remote(self, mock_subprocess_run):
        """Test successful creation of a project with a remote repo URL."""
        project_name = "remote-project"
        repo_url = "git@github.com:user/remote-project.git"
        projects_path_str = "projects"
        relative_project_path = Path(projects_path_str) / project_name

        mock_subprocess_run.return_value = subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr="")

        sys.argv = [
            'child_project_utils.py',
            project_name,
            '--repo-url', repo_url,
            '--path', projects_path_str
        ]

        with self.assertRaises(SystemExit) as cm:
            child_project_utils.main()
        self.assertEqual(cm.exception.code, 0)

        expected_calls = [
            call(['git', '--version'], check=True, capture_output=True),
            call(['git', 'init'], cwd=relative_project_path, check=True, capture_output=True, text=True, encoding='utf-8'),
            call(['git', 'remote', 'add', 'origin', repo_url], cwd=relative_project_path, check=True, capture_output=True, text=True, encoding='utf-8'),
            call(['git', 'add', '.'], cwd=relative_project_path, check=True, capture_output=True, text=True, encoding='utf-8'),
            call(['git', 'commit', '-m', 'Initial commit from scaffolding script'], cwd=relative_project_path, check=True, capture_output=True, text=True, encoding='utf-8'),
            call(['git', 'submodule', 'add', repo_url, str(relative_project_path)], cwd=None, check=True, capture_output=True, text=True, encoding='utf-8')
        ]
        mock_subprocess_run.assert_has_calls(expected_calls)

    @patch('sys.stderr')
    def test_failure_if_directory_exists(self, mock_stderr):
        """Test that the script fails if the target directory already exists."""
        project_name = "existing-project"
        projects_path = self.test_dir / "projects"
        project_path = projects_path / project_name
        project_path.mkdir(parents=True)

        sys.argv = [
            'child_project_utils.py',
            project_name,
            '--path', str(projects_path)
        ]

        with self.assertRaises(SystemExit) as cm:
            child_project_utils.main()
        
        self.assertEqual(cm.exception.code, 1)
        written_output = "".join(c.args[0] for c in mock_stderr.write.call_args_list)
        # Use the non-resolved path for assertion, as that's what the script prints.
        self.assertIn(f"Error: Directory '{project_path}' already exists.", written_output)

if __name__ == '__main__':
    unittest.main()
