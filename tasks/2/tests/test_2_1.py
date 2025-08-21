import os
import sys
import subprocess

def run():
    print("Running test for feature 2.1: Orchestrator script")
    script_path = "scripts/run_local_agent.py"

    # 1. Check if the script exists
    if not os.path.exists(script_path):
        print(f"FAIL: {script_path} does not exist.")
        sys.exit(1)

    # 2. Check for CLI options
    try:
        result = subprocess.run(
            [sys.executable, script_path, '--help'],
            capture_output=True,
            text=True,
            check=True
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        # The script might exit with an error because required args are missing, but --help should prevent that.
        # If it still fails, it's a problem.
        print(f"FAIL: Could not execute '{script_path} --help'. Error: {e}")
        if hasattr(e, 'stderr'):
            print(f"Stderr: {e.stderr}")
        sys.exit(1)

    help_output = result.stdout
    required_cli_args = ['--mode', '--task', '--feature']
    missing_cli_args = [arg for arg in required_cli_args if arg not in help_output]
    if missing_cli_args:
        print(f"FAIL: Missing required CLI arguments: {', '.join(missing_cli_args)}")
        sys.exit(1)

    # 3. Check for tool definitions (as strings in the file)
    with open(script_path, 'r') as f:
        content = f.read()
    
    # Note: 'move_task' is in acceptance criteria but not in the provided context file for run_local_agent.py.
    # The test will include it as per the task definition.
    required_tools = [
        'write_file',
        'retrieve_context_files',
        'rename_files',
        'submit_for_review',
        'ask_question',
        'finish',
        'finish_feature',
        # The acceptance criteria for 2.1 includes 'move_task' which is not in the provided script context.
        # This test will fail until it's added, which is the correct behavior.
        'move_task'
    ]
    missing_tools = [tool for tool in required_tools if f'def {tool}(' not in content and f'"{tool}"' not in content]
    if missing_tools:
        print(f"FAIL: Missing tool definitions in {script_path}: {', '.join(missing_tools)}")
        sys.exit(1)

    print("PASS: Orchestrator script exists, has required CLI options, and mentions all required tools.")
    sys.exit(0)

if __name__ == "__main__":
    run()
