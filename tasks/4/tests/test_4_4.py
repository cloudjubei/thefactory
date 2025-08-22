import os
import subprocess
import time

def test_docker_env_handling():
    # Create a temporary .env file
    env_content = 'TEST_API_KEY=test_value\n'
    with open('.env', 'w') as f:
        f.write(env_content)
    
    try:
        # Build the Docker image (assuming docker-compose.yml or Dockerfile is set up)
        subprocess.run(['docker-compose', 'build'], check=True)
        
        # Run the container in detached mode
        subprocess.run(['docker-compose', 'up', '-d'], check=True)
        
        # Wait a bit for the container to start
        time.sleep(5)
        
        # Get the container name or ID (assuming service name 'app')
        container_id = subprocess.check_output(['docker-compose', 'ps', '-q', 'app']).decode().strip()
        assert container_id, 'Container not running'
        
        # Check environment variables inside the container
        env_output = subprocess.check_output(['docker', 'exec', container_id, 'printenv']).decode()
        assert 'TEST_API_KEY=test_value' in env_output, 'TEST_API_KEY not found in container env'
        
        # Verify .env is not baked into the image (try to find it in container without mount)
        # Stop the container
        subprocess.run(['docker-compose', 'down'], check=True)
        
        # Run a new container without env_file or mount
        temp_container = subprocess.check_output([
            'docker', 'run', '-d', '--name', 'temp_test', 'your_image_name'  # Replace with actual image
        ]).decode().strip()
        
        # Check if .env exists in the container
        exit_code = subprocess.run(['docker', 'exec', temp_container, 'ls', '/app/.env'], capture_output=True).returncode
        assert exit_code != 0, '.env should not be present in the image'
        
        # Clean up
        subprocess.run(['docker', 'stop', 'temp_container'], check=True)
        subprocess.run(['docker', 'rm', 'temp_container'], check=True)
    
    finally:
        os.remove('.env')
        subprocess.run(['docker-compose', 'down'], check=True)