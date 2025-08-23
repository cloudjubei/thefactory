import os
import yaml
def run_tests():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    dir_path = os.path.join(base_dir, 'scripts', 'docker')
    file_path = os.path.join(dir_path, 'docker-compose.yml')
    assert os.path.isdir(dir_path), "Directory 'scripts/docker/' does not exist."
    assert os.path.isfile(file_path), "File 'scripts/docker/docker-compose.yml' does not exist."
    with open(file_path, 'r') as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            assert False, f"Invalid YAML: {e}"
    assert data is not None, "Empty YAML"
    assert 'version' in data, "No 'version' defined in docker-compose.yml"
    version_str = data['version']
    try:
        version_num = float(version_str)
        assert version_num >= 3, f"Compose version {version_num} is less than 3"
    except ValueError:
        assert False, f"Invalid version format: {version_str}"
    assert 'services' in data, "No 'services' section"
    assert 'agent' in data['services'], "No 'agent' service defined"
    agent = data['services']['agent']
    assert 'build' in agent, "No 'build' configuration for agent service"
    build = agent['build']
    if isinstance(build, str):
        assert build == '.', "Build is not set to local (.)"
    elif isinstance(build, dict):
        assert build.get('context') == '.', "Build context is not local"
    else:
        assert False, "Invalid build configuration"
    assert 'volumes' in agent, "No 'volumes' for agent service"
    volumes = agent['volumes']
    expected = {
        '../../.env:/app/.env',
        '../../projects:/app/projects',
        '../../tasks:/app/tasks'
    }
    actual = set()
    for vol in volumes:
        if isinstance(vol, str):
            parts = vol.split(':')
            if len(parts) >= 2:
                base_vol = ':'.join(parts[:2])
                actual.add(base_vol)
    for exp in expected:
        assert exp in actual, f"Missing volume mount: {exp}"
    print("All tests passed!")
if __name__ == "__main__":
    run_tests()
