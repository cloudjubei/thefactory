import unittest
import subprocess
import time
import json

class TestContainerIsolationPeriodic(unittest.TestCase):
    def test_periodic_isolated_run(self):
        # Build the Docker image
        subprocess.check_call(['docker', 'build', '-t', 'test-agent', '.'])

        # Run the container in detached mode
        container = subprocess.check_output(['docker', 'run', '-d', '--name', 'test-agent-container', 'test-agent']).decode().strip()

        try:
            # Wait for 70 seconds (assuming runs every 30s, expect at least 2 runs)
            time.sleep(70)

            # Get logs
            logs = subprocess.check_output(['docker', 'logs', container]).decode()

            # Check for multiple agent runs (assume agent logs 'Agent running' each time)
            run_count = logs.count('Agent running')
            self.assertGreaterEqual(run_count, 2, 'Agent did not run periodically')

            # Inspect container for isolation
            inspect_output = subprocess.check_output(['docker', 'inspect', container]).decode()
            inspect_data = json.loads(inspect_output)[0]
            self.assertFalse(inspect_data['HostConfig']['Privileged'], 'Container should not run in privileged mode')
            self.assertEqual(inspect_data['HostConfig']['Binds'], [], 'No host binds should be present')

        finally:
            # Cleanup
            subprocess.call(['docker', 'stop', container])
            subprocess.call(['docker', 'rm', container])