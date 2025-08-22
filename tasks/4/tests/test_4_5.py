import subprocess
import time
import re
from pathlib import Path

def run_command(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

def test_periodic_execution():
    # Cleanup existing container and image if any
    run_command(['docker', 'stop', 'test-container'])
    run_command(['docker', 'rm', 'test-container'])
    run_command(['docker', 'rmi', 'test-agent'])
    dockerfile_path = Path('docs/docker/Dockerfile')
    entrypoint_path = Path('entrypoint.sh')
    assert dockerfile_path.exists()
    assert entrypoint_path.exists()
    docker_content = dockerfile_path.read_text()
    entrypoint_content = entrypoint_path.read_text()
    # Check mechanism: loop in entrypoint
    assert 'while true' in entrypoint_content
    assert 'sleep' in entrypoint_content
    # Check isolation: USER in Dockerfile, no VOLUME
    assert 'USER appuser' in docker_content
    assert 'VOLUME' not in docker_content
    # Build image
    build_result = run_command(['docker', 'build', '-t', 'test-agent', '-f', 'docs/docker/Dockerfile', '.'])
    assert build_result.returncode == 0, build_result.stderr
    # Run container with short interval and test mode
    run_result = run_command(['docker', 'run', '-d', '--name', 'test-container', '-e', 'SLEEP_INTERVAL=1', '-e', 'TEST_MODE=1', 'test-agent'])
    assert run_result.returncode == 0, run_result.stderr
    # Wait for at least 3 runs (1s sleep, wait 5s)
    time.sleep(5)
    # Get logs
    logs_result = run_command(['docker', 'logs', 'test-container'])
    assert logs_result.returncode == 0
    logs = logs_result.stdout
    # Count executions
    count = len(re.findall(r'Test run at', logs))
    assert count >= 3, f"Expected at least 3 executions, found {count}"
    # Cleanup
    run_command(['docker', 'stop', 'test-container'])
    run_command(['docker', 'rm', 'test-container'])
    run_command(['docker', 'rmi', 'test-agent'])
    print("All tests passed!")

if __name__ == "__main__":
    test_periodic_execution()