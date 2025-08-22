import os

def test_readme():
    path = 'docs/docker/RUNNING_DOCKER_README.md'
    assert os.path.exists(path), 'README file does not exist'
    with open(path, 'r') as f:
        content = f.read().lower()
    assert '.env' in content, 'No instructions for preparing .env'
    assert 'build script' in content or 'build_docker.sh' in content, 'No steps to use the build script'
    assert 'periodically' in content or 'cron' in content, 'No instructions on running the container periodically'

if __name__ == '__main__':
    test_readme()
    print('Test passed')
