import os
import re

def test_build_docker_script():
    script_path = 'scripts/build_docker.sh'
    assert os.path.exists(script_path), 'Build script does not exist'
    assert os.access(script_path, os.X_OK), 'Script is not executable'
    with open(script_path, 'r') as f:
        content = f.read()
    assert content.startswith('#!/bin/'), 'Missing shebang'
    assert 'git clone' in content, 'Missing git clone command'
    assert re.search(r'if\s*\[\s*!\s*-f\s*\.env\s*\]', content) or 'if [ ! -f .env ]' in content, 'Missing .env file check'
    assert 'docker build' in content, 'Missing docker build command'
    assert 'docker run' in content, 'Missing instructions for running the container'