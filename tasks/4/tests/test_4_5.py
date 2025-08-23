import os

def test_docker_setup():
    file_path = 'docs/DOCKER_SETUP.md'
    assert os.path.exists(file_path), f"{file_path} does not exist"
    with open(file_path, 'r') as f:
        content = f.read()
    assert 'Prerequisites' in content, "Missing 'Prerequisites' section"
    assert 'Docker' in content, "Missing mention of Docker in prerequisites"
    assert 'Docker Compose' in content, "Missing mention of Docker Compose in prerequisites"
    assert 'scripts/docker/run.sh' in content, "Missing instructions for using run.sh"
    assert 'Example' in content, "Missing example usage"
    assert 'interact with the agent' in content, "Missing information on interacting with the agent"
    print("Tests passed")