import unittest
import shutil
import subprocess
import os
from pathlib import Path
import tempfile

class TestEnvFileHandling(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp()
        current_repo = Path('.').resolve()
        subprocess.run(['git', 'clone', str(current_repo), cls.temp_dir], check=True)
        cls.old_cwd = os.getcwd()
        os.chdir(cls.temp_dir)
        cls.script = 'scripts/child_project_utils.py'
        cls.projects_dir = Path('projects')

    @classmethod
    def tearDownClass(cls):
        os.chdir(cls.old_cwd)
        shutil.rmtree(cls.temp_dir)

    def setUp(self):
        self.test_project = 'test_child_' + str(id(self))[-6:]
        self.child_dir = self.projects_dir / self.test_project

    def run_script(self, *args):
        cmd = ['python3', self.script, self.test_project] + list(args)
        return subprocess.run(cmd, capture_output=True, text=True, check=False)

    def tearDown(self):
        if self.child_dir.exists():
            subprocess.run(['git', 'submodule', 'deinit', '-f', str(self.child_dir)], check=False)
            subprocess.run(['git', 'rm', '-f', str(self.child_dir)], check=False)
            Path('.git/modules/' + str(self.child_dir)).rmtree_p() if Path('.git/modules/' + str(self.child_dir)).exists() else None
            shutil.rmtree(self.child_dir, ignore_errors=True)

    def test_copy_without_repo_url(self):
        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stderr)
        env_path = self.child_dir / '.env'
        self.assertTrue(env_path.exists())
        parent_env = Path('.env')
        self.assertEqual(env_path.read_text(), parent_env.read_text())

    def test_with_repo_url(self):
        repo_url = 'https://example.com/test-repo.git'
        result = self.run_script('--repo-url', repo_url)
        self.assertEqual(result.returncode, 0, result.stderr)
        env_path = self.child_dir / '.env'
        self.assertTrue(env_path.exists())
        content = env_path.read_text()
        self.assertIn(f'GIT_REPO_URL="{repo_url}"', content)
        parent_content = Path('.env').read_text()
        parent_without_git = '\n'.join([line for line in parent_content.splitlines() if not line.startswith('GIT_REPO_URL=')]) + '\n'
        child_without_git = '\n'.join([line for line in content.splitlines() if not line.startswith('GIT_REPO_URL=')]) + '\n'
        self.assertEqual(child_without_git, parent_without_git)

    def test_no_parent_env(self):
        parent_env = Path('.env')
        if parent_env.exists():
            parent_env.unlink()
        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('warn', result.stderr.lower())
        env_path = self.child_dir / '.env'
        self.assertTrue(env_path.exists())
        content = env_path.read_text()
        self.assertIn('GIT_REPO_URL=""', content)

    def test_no_parent_env_with_url(self):
        parent_env = Path('.env')
        if parent_env.exists():
            parent_env.unlink()
        repo_url = 'https://example.com/test-repo.git'
        result = self.run_script('--repo-url', repo_url)
        self.assertEqual(result.returncode, 0, result.stderr)
        env_path = self.child_dir / '.env'
        self.assertTrue(env_path.exists())
        content = env_path.read_text()
        self.assertIn(f'GIT_REPO_URL="{repo_url}"', content)

    def test_env_committed(self):
        self.run_script()
        committed_files = subprocess.run(['git', 'ls-tree', '-r', 'HEAD', '--name-only'], cwd=self.child_dir, capture_output=True, text=True).stdout.splitlines()
        self.assertIn('.env', committed_files)

    def test_documentation_updated(self):
        doc_path = Path('docs/PROJECTS_GUIDE.md')
        content = doc_path.read_text().lower()
        self.assertIn('the .env is copied from the parent', content)
        self.assertIn('git_repo_url is overridden if --repo-url is used', content)
        self.assertIn('example in the script usage section', content)

    def test_error_handling_copy_fail(self):
        parent_env = Path('.env')
        if not parent_env.exists():
            parent_env.write_text('GIT_REPO_URL="test"\n')
        original_mode = parent_env.stat().st_mode
        parent_env.chmod(0o000)  # Make unreadable to simulate copy failure
        try:
            result = self.run_script()
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('error', result.stderr.lower())
        finally:
            parent_env.chmod(original_mode)

if __name__ == '__main__':
    unittest.main()