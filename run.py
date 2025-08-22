import argparse
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

IGNORE_PATTERNS = shutil.ignore_patterns('.git', 'venv', '__pycache__', '*.pyc', '.idea')

def main():
    """
    Main launcher for the AI agent. It must be run from the project's root directory.
    It creates a temporary, isolated copy of the repository and then
    executes the agent orchestrator script (`scripts/run_local_agent.py`) inside it.
    """
    parser = argparse.ArgumentParser(description="Launcher for the autonomous AI agent.")
    parser.add_argument("--model", type=str, default="gpt-4-turbo-preview", help="LLM model name.")
    parser.add_argument("--agent", type=str, required=True, choices=['developer', 'tester', 'planner', 'contexter'], help="Agent persona.")
    parser.add_argument("--task", type=int, help="Optional: Specify a task ID to work on.")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent

    with tempfile.TemporaryDirectory() as temp_dir_str:
        temp_dir = Path(temp_dir_str)
        workspace_path = temp_dir / "workspace"
        
        print(f"Copying repository from '{project_root}' to temporary workspace: '{workspace_path}'")

        try:
            shutil.copytree(project_root, workspace_path, ignore=IGNORE_PATTERNS)
        except Exception as e:
            print(f"FATAL: Failed to copy repository to temporary directory: {e}")
            return

        orchestrator_script_path = workspace_path / "scripts" / "run_local_agent.py"

        command = [
            "python3",
            str(orchestrator_script_path),
            "--agent", args.agent,
            "--model", args.model
        ]
        if args.task:
            command.extend(["--task", str(args.task)])

        print(f"Executing command: {' '.join(command)}")

        try:
            subprocess.run(command, cwd=workspace_path, check=True)
        except subprocess.CalledProcessError as e:
            print(f"\n--- An error occurred while running the agent orchestrator: {e} ---")
        except KeyboardInterrupt:
            print("\n--- Agent run interrupted by user. ---")

    print("\n--- Agent run finished. Temporary directory cleaned up. ---")

if __name__ == "__main__":
    main()