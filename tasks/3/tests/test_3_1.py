import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT_PATH = Path(__file__).resolve().parents[3] / 'scripts' / 'child_project_utils.py'
REPO_ROOT = Path(__file__).resolve().parents[3]


def run(cmd, cwd=None, check=True, env=None):
    return subprocess.run(cmd, cwd=cwd, check=check, text=True, capture_output=True, env=env)


def ensure_git_repo(path: Path):
    run(['git', 'init'], cwd=path)
    # local config to avoid author errors
    run(['git', 'config', 'user.name', 'Test User'], cwd=path)
    run(['git', 'config', 'user.email', 'test@example.com'], cwd=path)


def common_env():
    env = os.environ.copy()
    env.update({
        'GIT_AUTHOR_NAME': 'Test User',
        'GIT_AUTHOR_EMAIL': 'test@example.com',
        'GIT_COMMITTER_NAME': 'Test User',
        'GIT_COMMITTER_EMAIL': 'test@example.com',
    })
    return env


def seed_example_docs(temp_root: Path):
    docs_tasks = temp_root / 'docs' / 'tasks'
    docs_tasks.mkdir(parents=True, exist_ok=True)
    src = REPO_ROOT / 'docs' / 'tasks' / 'task_example.json'
    assert src.exists(), 'Source docs/tasks/task_example.json missing in repo under test.'
    shutil.copy2(src, docs_tasks / 'task_example.json')


def read_json(p: Path):
    with p.open('r', encoding='utf-8') as f:
        return json.load(f)


@pytest.fixture()
def temp_superproject(tmp_path):
    sp = tmp_path / 'super'
    sp.mkdir()
    ensure_git_repo(sp)
    # create an initial commit so submodule metadata changes can be diffed if needed
    (sp / '.gitignore').write_text('\n', encoding='utf-8')
    run(['git', 'add', '.'], cwd=sp)
    run(['git', 'commit', '-m', 'init'], cwd=sp)
    seed_example_docs(sp)
    return sp


def test_help_message():
    # Running help should succeed and include usage and options
    proc = run([sys.executable, str(SCRIPT_PATH), '-h'], check=False)
    assert proc.returncode == 0
    assert 'usage' in proc.stdout.lower()
    assert '--task-id' in proc.stdout


def test_dry_run_no_side_effects(temp_superproject):
    sp = temp_superproject
    env = common_env()
    proj_name = 'dryrun_proj'
    proc = run([sys.executable, str(SCRIPT_PATH), proj_name, '--dry-run', '--description', 'Desc', '--path', 'projects'], cwd=sp, check=False, env=env)
    assert proc.returncode == 0
    # Ensure no directories created
    assert not (sp / 'projects' / proj_name).exists(), 'Dry run should not create project directory.'
    # Print should include DRY RUN markers
    assert 'DRY RUN' in proc.stdout


def test_create_project_default_task(temp_superproject):
    sp = temp_superproject
    env = common_env()
    proj_name = 'alpha'
    desc = 'A new child project alpha.'
    # Execute
    proc = run([sys.executable, str(SCRIPT_PATH), proj_name, '--description', desc, '--path', 'projects'], cwd=sp, check=False, env=env)
    assert proc.returncode == 0, proc.stderr

    proj_path = sp / 'projects' / proj_name
    # Structure exists
    assert proj_path.exists()
    assert (proj_path / 'README.md').exists()
    assert desc in (proj_path / 'README.md').read_text(encoding='utf-8')
    assert (proj_path / '.gitignore').exists()
    # tasks/1/task.json exists and is valid JSON
    task_json_path = proj_path / 'tasks' / '1' / 'task.json'
    assert task_json_path.exists(), 'tasks/1/task.json must be created.'
    data = read_json(task_json_path)
    assert isinstance(data, dict)
    assert 'features' in data and isinstance(data['features'], list)

    # Child repo initialized and clean
    assert (proj_path / '.git').exists(), 'Child .git folder should exist.'
    status = run(['git', 'status', '--porcelain'], cwd=proj_path).stdout.strip()
    assert status == '', f'Child repo should be clean after initial commit, got: {status}'

    # Submodule recorded in parent (.gitmodules updated)
    gm = sp / '.gitmodules'
    assert gm.exists(), '.gitmodules should be created in the superproject.'
    gm_text = gm.read_text(encoding='utf-8')
    assert f'path = projects/{proj_name}' in gm_text


def test_idempotent_re_run_fails_fast(temp_superproject):
    sp = temp_superproject
    env = common_env()
    proj_name = 'idem_proj'
    # First run succeeds
    proc1 = run([sys.executable, str(SCRIPT_PATH), proj_name, '--path', 'projects'], cwd=sp, check=False, env=env)
    assert proc1.returncode == 0, proc1.stderr
    # Second run must fail fast with clear message and not alter .gitmodules further
    gm_before = (sp / '.gitmodules').read_text(encoding='utf-8') if (sp / '.gitmodules').exists() else ''
    proc2 = run([sys.executable, str(SCRIPT_PATH), proj_name, '--path', 'projects'], cwd=sp, check=False, env=env)
    assert proc2.returncode != 0, 'Re-running with same project name should fail with non-zero exit code.'
    assert 'already exists' in (proc2.stderr + proc2.stdout).lower()
    gm_after = (sp / '.gitmodules').read_text(encoding='utf-8') if (sp / '.gitmodules').exists() else ''
    assert gm_before == gm_after, '.gitmodules should not be altered on idempotent failure.'


def test_remote_origin_is_set_when_provided(temp_superproject, tmp_path):
    sp = temp_superproject
    env = common_env()
    # Create a local bare repo to act as remote
    bare = tmp_path / 'remote_repo.git'
    run(['git', 'init', '--bare', str(bare)])
    repo_url = f'file://{bare}'

    proj_name = 'gamma'
    proc = run([sys.executable, str(SCRIPT_PATH), proj_name, '--repo-url', repo_url, '--path', 'projects'], cwd=sp, check=False, env=env)
    assert proc.returncode == 0, proc.stderr

    proj_path = sp / 'projects' / proj_name
    # Check origin set
    origin = run(['git', 'remote', 'get-url', 'origin'], cwd=proj_path).stdout.strip()
    assert origin == repo_url

    # Submodule URL in .gitmodules should match
    gm_text = (sp / '.gitmodules').read_text(encoding='utf-8')
    assert f'url = {repo_url}' in gm_text


def test_task_id_copy_and_rewrite(temp_superproject):
    sp = temp_superproject
    env = common_env()
    # Seed a source task folder tasks/42/task.json in the superproject
    src_task_dir = sp / 'tasks' / '42'
    src_task_dir.mkdir(parents=True)
    src_task = {
        'id': 42,
        'title': 'Sample task 42',
        'status': '-',
        'description': 'Demo',
        'features': [
            {'id': '42.1', 'status': '-', 'title': 'F1', 'description': 'd', 'plan': '', 'context': [], 'acceptance': []},
            {'id': '42.10', 'status': '-', 'title': 'F10', 'description': 'd', 'plan': '', 'context': [], 'acceptance': []},
        ],
    }
    (src_task_dir / 'task.json').write_text(json.dumps(src_task, indent=2), encoding='utf-8')

    proj_name = 'beta'
    proc = run([sys.executable, str(SCRIPT_PATH), proj_name, '--path', 'projects', '--task-id', '42'], cwd=sp, check=False, env=env)
    assert proc.returncode == 0, proc.stderr

    child_task_json = sp / 'projects' / proj_name / 'tasks' / '1' / 'task.json'
    assert child_task_json.exists()
    data = read_json(child_task_json)
    # id rewritten to 1
    assert data['id'] == 1
    # feature ids rewritten to start with '1.' and preserve suffix
    fids = [f['id'] for f in data['features']]
    assert all(fid.startswith('1.') for fid in fids)
    assert '1.1' in fids and '1.10' in fids
