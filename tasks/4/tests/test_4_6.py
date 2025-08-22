import os
import sys
import tempfile
import subprocess

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(project_root)

from scripts.git_manager import GitManager

def test_git_workflow():
    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"Temporary directory: {tmpdir}")
        try:
            subprocess.run(["git", "init", tmpdir], check=True, capture_output=True)
            print("Git repo initialized.")
        except Exception as e:
            raise RuntimeError(f"Failed at git init: {e}")
        try:
            gm = GitManager(tmpdir)
            print("GitManager created and configured.")
        except Exception as e:
            raise RuntimeError(f"Failed at GitManager init: {e}")
        try:
            test_file = os.path.join(tmpdir, 'test.txt')
            with open(test_file, 'w') as f:
                f.write('Initial content')
            print("Test file created.")
        except Exception as e:
            raise RuntimeError(f"Failed at file creation: {e}")
        try:
            gm.stage_files(['test.txt'])
            print("Files staged.")
        except Exception as e:
            raise RuntimeError(f"Failed at staging: {e}")
        try:
            commit_result = gm.commit('Initial commit')
            print(f"Initial commit result: {commit_result}")
            assert 'nothing to commit' not in commit_result.lower(), "Initial commit failed"
        except Exception as e:
            raise RuntimeError(f"Failed at initial commit: {e}")
        try:
            branch_name = 'features/test'
            gm.create_branch_and_checkout(branch_name)
            print("Branch created and checked out.")
        except Exception as e:
            raise RuntimeError(f"Failed at branch creation: {e}")
        try:
            current_branch = gm.get_current_branch()
            assert current_branch == branch_name, f"Expected {branch_name}, got {current_branch}"
            print("Branch assertion passed.")
        except Exception as e:
            raise RuntimeError(f"Failed at branch assertion: {e}")
        try:
            with open(test_file, 'a') as f:
                f.write('\nAdditional content')
            print("File modified.")
        except Exception as e:
            raise RuntimeError(f"Failed at file modification: {e}")
        try:
            gm.stage_files(['.'])
            print("Changes staged.")
        except Exception as e:
            raise RuntimeError(f"Failed at staging changes: {e}")
        try:
            commit_result = gm.commit('Completed task test')
            print(f"Task commit result: {commit_result}")
            assert 'nothing to commit' not in commit_result.lower(), "Commit failed"
        except Exception as e:
            raise RuntimeError(f"Failed at task commit: {e}")
        try:
            commit_result = gm.commit('No change')
            print(f"No change commit result: {commit_result}")
            assert 'nothing to commit' in commit_result.lower(), "Expected nothing to commit handling"
        except Exception as e:
            raise RuntimeError(f"Failed at no change commit: {e}")
    print("Git workflow test passed.")

def test_git_in_docker():
    try:
        build_output = subprocess.check_output(["docker", "build", "-q", "-t", "agent-test", "."], cwd=project_root)
        assert build_output.strip(), "Docker build failed"
        result = subprocess.check_output(["docker", "run", "--rm", "--entrypoint", "git", "agent-test", "--version"])
        assert b"git version" in result, "Git not found in Docker image"
        print("Git is installed in the Docker image.")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Docker test failed: {e}")

if __name__ == '__main__':
    try:
        test_git_workflow()
        test_git_in_docker()
        print("All tests passed.")
        sys.exit(0)
    except Exception as e:
        print(f"Test failed: {e}")
        sys.exit(1)