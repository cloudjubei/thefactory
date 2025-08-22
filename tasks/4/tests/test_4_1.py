import os

def test_dockerfile_exists():
    assert os.path.exists('docs/docker/Dockerfile')

def test_dockerfile_content():
    path = 'docs/docker/Dockerfile'
    with open(path, 'r') as f:
        content = f.read()
    assert 'FROM python' in content, 'Missing Python base image'
    assert 'pip install -r requirements.txt' in content, 'Missing dependency installation'
    assert 'COPY ' in content, 'Missing file copy instructions'
    assert '.env' in content, 'Missing .env handling'
    assert 'ENTRYPOINT' in content or 'CMD' in content, 'Missing entrypoint or cmd for running the agent'