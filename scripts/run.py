import argparse
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

IGNORE_PATTERNS = shutil.ignore_patterns('.git', 'venv', '__pycache__', '*.pyc', '.idea')

def main():
    """
    This is the main launcher for the AI agent.
    It creates a temporary, isolated copy of the repository and then
    executes the main agent orchestrator script (`run_local_agent.py`) inside it.
    """
    parser = argparse.ArgumentParser(description="Launcher for the autonomous AI agent.")
    parser.add_argument("--model", type=str, default="gpt-5", help="LLM model name.")
    parser.add_argument("--agent", type=str, required=True, choices=['developer', 'tester', 'planner', 'contexter'], help="Agent persona.")
    parser.add_argument("--task", type=int, help="Optional: Specify a task ID to work on.")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_project_root = Path(temp_dir)
        print(f"--- Created temporary directory for agent run: {temp_project_root} ---")

        print("Copying repository to temporary directory...")
        shutil.copytree(project_root, temp_project_root, dirs_exist_ok=True, ignore=IGNORE_PATTERNS)

        orchestrator_script_path = temp_project_root / "scripts" / "run_local_agent.py"
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
            subprocess.run(command, cwd=temp_project_root, check=True)
        except subprocess.CalledProcessError as e:
            print(f"\n--- An error occurred while running the agent orchestrator: {e} ---")
        except KeyboardInterrupt:
            print("\n--- Agent run interrupted by user. ---")

    print("\n--- Agent run finished. Temporary directory cleaned up. ---")

if __name__ == "__main__":
    main()