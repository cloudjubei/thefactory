import os
import sys

def run_test():
    """
    Tests that docs/docker/RUNNING_DOCKER_README.md and docs/docker/Dockerfile exist.
    """
    readme_path = "docs/docker/RUNNING_DOCKER_README.md"
    dockerfile_path = "docs/docker/Dockerfile"

    # 1. Check for file existence
    if not os.path.exists(readme_path):
        print(f"FAIL: {readme_path} does not exist.")
        sys.exit(1)

    if not os.path.exists(dockerfile_path):
        print(f"FAIL: {dockerfile_path} does not exist.")
        sys.exit(1)
        
    # Optional: Basic content check for Dockerfile (e.g., 'FROM python')
    try:
        with open(dockerfile_path, 'r') as f:
            content = f.read()
            if "FROM python" not in content and "FROM" not in content:
                print(f"FAIL: {dockerfile_path} does not contain 'FROM python' or generic 'FROM' statement.")
                sys.exit(1)
    except Exception as e:
        print(f"FAIL: Could not read {dockerfile_path}: {e}")
        sys.exit(1)

    print(f"PASS: {readme_path} and {dockerfile_path} exist and contain basic expected content.")
    sys.exit(0)

if __name__ == "__main__":
    run_test()
