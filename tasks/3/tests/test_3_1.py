import os
import subprocess
import shutil
import tempfile
from pathlib import Path
import unittest
import sys

class TestChildProjectUtils(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = self.tmpdir.name
        self.scripts_dir = os.path.join(self.root, 'scripts')
        os.mkdir(self.scripts_dir)
        shutil.copy(os.path.abspath('scripts/child_project_utils.py'), os.path.join(self.scripts_dir, 'child_project_utils.py'))
        subprocess.check_call(['git', 'init', '-q'], cwd=self.root)
        self.original_cwd = os.getcwd()
        os.chdir(self.root)

    def tearDown(self):
        os.chdir(self.original_cwd)
        self.tmpdir.cleanup()

    def run_script(self, args, env=None):
        cmd = [sys.executable, 'scripts/child_project_utils.py'] + args
        return subprocess.run(cmd, capture_output=True, text=True, env=env)

    def test_1_and_10_cli_and_help(self):
        result = self.run_script(['-h'])
        self.assertEqual(result.returncode, 0)
        help_text = result.stdout
        self.assertIn('project_name', help_text)
        self.assertIn('--description', help_text)
        self.assertIn('--repo-url', help_text)
        self.assertIn('--path', help_text)
        self.assertIn('--dry-run', help_text)
        self.assertIn('Examples:', help_text)

    def test_8_dry_run(self):
        project_name = 'dry_proj'
        result = self.run_script([project_name, '--dry-run'])
        self.assertEqual(result.returncode, 0)
        proj_path = f'projects/{project_name}'
        self.assertFalse(os.path.exists(proj_path))
        self.assertIn('DRY RUN', result.stdout)
        self.assertIn('git init', result.stdout)
        self.assertIn('git add .', result.stdout)
        self.assertIn('git commit', result.stdout)
        self.assertIn('git submodule add', result.stdout)

    def test_2_3_4_6_7_9_new_project_local(self):
        project_name = 'local_proj'
        result = self.run_script([project_name])
        self.assertEqual(result.returncode, 0, result.stderr)
        proj_path = f'projects/{project_name}'
        self.assertTrue(os.path.isdir(proj_path))
        # 3
        self.assertTrue(os.path.exists(f'{proj_path}/README.md'))
        with open(f'{proj_path}/README.md') as f:
            content = f.read()
            self.assertIn(project_name, content)
            self.assertIn('A new child project.', content)
        self.assertTrue(os.path.isdir(f'{proj_path}/tasks'))
        self.assertTrue(os.path.exists(f'{proj_path}/tasks/000_initial_task.md'))
        with open(f'{proj_path}/tasks/000_initial_task.md') as f:
            content = f.read()
            self.assertIn('Initial Task', content)
        self.assertTrue(os.path.exists(f'{proj_path}/.gitignore'))
        with open(f'{proj_path}/.gitignore') as f:
            content = f.read()
            self.assertIn('__pycache__', content)
            self.assertIn('node_modules/', content)
        # 4
        self.assertTrue(os.path.isdir(f'{proj_path}/.git'))
        status = subprocess.run(['git', 'status', '--porcelain'], cwd=proj_path, capture_output=True, text=True)
        self.assertEqual(status.stdout, '')
        log = subprocess.run(['git', 'log', '--oneline'], cwd=proj_path, capture_output=True, text=True)
        self.assertIn('Initial commit', log.stdout)
        remotes = subprocess.run(['git', 'remote'], cwd=proj_path, capture_output=True, text=True)
        self.assertEqual(remotes.stdout, '')
        # 6
        sub_status = subprocess.run(['git', 'submodule', 'status', proj_path], capture_output=True, text=True)
        self.assertEqual(sub_status.returncode, 0)
        self.assertTrue(sub_status.stdout.strip())
        self.assertTrue(os.path.exists('.gitmodules'))
        with open('.gitmodules') as f:
            content = f.read()
            self.assertIn(f'[submodule "{proj_path}"]', content)
            self.assertIn(f'path = {proj_path}', content)
            self.assertIn(f'url = ./{proj_path}', content)
        # 7
        result2 = self.run_script([project_name])
        self.assertNotEqual(result2.returncode, 0)
        self.assertIn('already exists', result2.stderr)

    def test_5_and_6_with_repo_url(self):
        project_name = 'remote_proj'
        bare_path = os.path.join(self.root, 'bare.git')
        subprocess.check_call(['git', 'init', '--bare', bare_path])
        result = self.run_script([project_name, '--repo-url', bare_path])
        self.assertEqual(result.returncode, 0, result.stderr)
        proj_path = f'projects/{project_name}'
        remote_url = subprocess.run(['git', 'remote', 'get-url', 'origin'], cwd=proj_path, capture_output=True, text=True)
        self.assertEqual(remote_url.stdout.strip(), bare_path)
        with open('.gitmodules') as f:
            content = f.read()
            self.assertIn(f'url = {bare_path}', content)

    def test_9_missing_git(self):
        project_name = 'some_proj'
        empty_bin = os.path.join(self.root, 'empty_bin')
        os.mkdir(empty_bin)
        env = os.environ.copy()
        env['PATH'] = empty_bin
        result = self.run_script([project_name], env=env)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('git', result.stderr.lower())
        self.assertIn('not found', result.stderr.lower() or 'command not found' in result.stderr.lower())

if __name__ == '__main__':
    unittest.main()