import os

def test_dockerignore():
    path = 'scripts/docker/.dockerignore'
    assert os.path.exists(path), f'{path} does not exist'
    with open(path, 'r') as f:
        di_lines = set(line.strip() for line in f if line.strip() and not line.startswith('#'))
    with open('.gitignore', 'r') as f:
        git_lines = set(line.strip() for line in f if line.strip() and not line.startswith('#') and not line.startswith('!'))
    additional = {'.git', '.venv', 'tasks/'}
    required = git_lines | additional
    missing = required - di_lines
    assert not missing, f'Missing required ignore patterns: {missing}'
    # Check no absolute paths
    absolute = [line for line in di_lines if line.startswith('/')]
    assert not absolute, f'Absolute paths found in .dockerignore: {absolute}'

if __name__ == '__main__':
    test_dockerignore()