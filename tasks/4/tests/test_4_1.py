import os

def test_dockerfile():
    docker_dir = 'scripts/docker'
    dockerfile_path = os.path.join(docker_dir, 'Dockerfile')
    
    # Criterion 1
    assert os.path.exists(docker_dir), "Directory 'scripts/docker' does not exist."
    
    # Criterion 2
    assert os.path.isfile(dockerfile_path), "File 'Dockerfile' does not exist in 'scripts/docker/'."
    
    with open(dockerfile_path, 'r') as f:
        content = f.read().lower()
    
    # Criterion 3
    assert 'from python:3.11-slim' in content, "Dockerfile does not use 'python:3.11-slim' as base image."
    
    # Criterion 4
    assert 'workdir' in content, "Dockerfile does not set a working directory."
    
    # Criterion 5
    assert 'copy ' in content, "Dockerfile does not copy project files."
    
    # Criterion 6
    assert 'run pip install -r requirements.txt' in content, "Dockerfile does not install dependencies from requirements.txt."
    
    print("All criteria passed.")

test_dockerfile()