import os
import yaml

def test_docker_compose():
    # Criterion 1: The directory 'scripts/docker/' exists in the project root.
    assert os.path.isdir('scripts/docker'), "Directory 'scripts/docker/' does not exist."
    
    # Criterion 2: The file 'scripts/docker/docker-compose.yml' exists.
    compose_path = 'scripts/docker/docker-compose.yml'
    assert os.path.isfile(compose_path), f"File '{compose_path}' does not exist."
    
    # Criterion 3: The 'docker-compose.yml' file is valid YAML and defines a compose version (e.g., '3' or higher).
    with open(compose_path, 'r') as f:
        content = yaml.safe_load(f)
    assert isinstance(content, dict), "docker-compose.yml is not valid YAML (not a dictionary)."
    assert 'version' in content, "No 'version' defined in docker-compose.yml."
    version_str = content['version']
    try:
        version_num = float(version_str)
        assert version_num >= 3, f"Compose version '{version_str}' is less than 3."
    except ValueError:
        assert False, f"Invalid compose version '{version_str}'."
    
    # Criterion 4: The file defines a service named 'agent'.
    assert 'services' in content, "No 'services' section in docker-compose.yml."
    assert 'agent' in content['services'], "No 'agent' service defined."
    agent_service = content['services']['agent']
    
    # Criterion 5: The 'agent' service has a build configuration that uses the local Dockerfile.
    assert 'build' in agent_service, "No 'build' configuration in 'agent' service."
    build_config = agent_service['build']
    if isinstance(build_config, str):
        assert build_config == '.', "Build config should be '.' for local Dockerfile."
    elif isinstance(build_config, dict):
        assert 'context' in build_config and 'dockerfile' in build_config, "Build dict must have 'context' and 'dockerfile'."
    else:
        assert False, "Invalid 'build' configuration type."
    
    # Criterion 6-8: Check volume mounts
    assert 'volumes' in agent_service, "No 'volumes' section in 'agent' service."
    volumes = agent_service['volumes']
    assert isinstance(volumes, list), "'volumes' is not a list."
    
    # Check for .env mount
    env_mounted = any(v.startswith('../../.env:') and v.endswith('/.env') for v in volumes if isinstance(v, str))
    assert env_mounted, "No volume mount for '../../.env' to a container path ending with '/.env'."
    
    # Check for projects/ mount
    projects_mounted = any(v.startswith('../../projects:') and v.endswith('/projects') for v in volumes if isinstance(v, str))
    assert projects_mounted, "No volume mount for '../../projects' to a container path ending with '/projects'."
    
    # Check for tasks/ mount
    tasks_mounted = any(v.startswith('../../tasks:') and v.endswith('/tasks') for v in volumes if isinstance(v, str))
    assert tasks_mounted, "No volume mount for '../../tasks' to a container path ending with '/tasks'."
    
if __name__ == '__main__':
    test_docker_compose()
    print('All tests passed.')
