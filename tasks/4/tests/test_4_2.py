import os

def test_docker_readme():
    file_path = 'docs/docker/RUNNING_DOCKER_README.md'
    assert os.path.exists(file_path), 'README file does not exist'
    with open(file_path, 'r') as f:
        content = f.read().lower()
    assert '.env' in content and 'prepare' in content, 'No instructions for preparing .env'
    assert 'build script' in content, 'No instructions for using the build script'
    assert 'run' in content and 'container' in content and 'periodically' in content, 'No instructions for running container periodically'