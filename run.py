import argparse
import os
import shutil
import subprocess
import tempfile
import traceback
from pathlib import Path

IGNORE_PATTERNS = shutil.ignore_patterns('venv', '__pycache__', '*.pyc', '.idea')

DEPRECATION_BANNER = """
[DEPRECATION NOTICE]
The Python orchestrator is deprecated. The TypeScript implementation is now the primary path.
Prefer the Node CLI:
  npx -y tsx scripts/runAgent.ts --project-root . --task-id <id>
See docs/RUN_AGENT_CLI.md for details.

This launcher will attempt to delegate to the Node CLI automatically when available.
Set FACTORY_FORCE_PYTHON=1 or FACTORY_BRIDGE_TO_NODE=0 to skip delegation.
""".strip()

def try_bridge_to_node(project_root: Path, task: str | None, project_dir: str | None) -> bool:
    """
    Attempt to delegate execution to the Node CLI. Returns True if the Node run was invoked
    (regardless of success), False if delegation was not attempted.
    On success (exit code 0), we return True to signal that no legacy path is needed.
    On failure (non-zero exit code), we return False to fall back to Python.
    """
    # Respect environment flags
    if os.getenv("FACTORY_FORCE_PYTHON") == "1" or os.getenv("FACTORY_BRIDGE_TO_NODE") == "0":
        return False

    node_cmd_override = os.getenv("FACTORY_NODE_CMD")
    # Prefer a direct npx tsx invocation so no local install is required
    if node_cmd_override:
        base_cmd = node_cmd_override.split()
    else:
        base_cmd = ["npx", "-y", "tsx", "scripts/runAgent.ts"]

    # Map a minimal subset of arguments to the Node CLI
    args = []
    # project-root
    if project_dir:
        args += ["--project-root", str((project_root / project_dir).resolve())]
    else:
        args += ["--project-root", str(project_root.resolve())]
    # task-id
    if task:
        args += ["--task-id", str(task)]

    print("\n[Bridge] Delegating to Node CLI:")
    print(" ", " ".join(base_cmd + args))

    try:
        result = subprocess.run(base_cmd + args, cwd=project_root, check=False)
        if result.returncode == 0:
            print("[Bridge] Node CLI completed successfully. Skipping legacy Python run.")
            return True
        else:
            print(f"[Bridge] Node CLI exited with code {result.returncode}. Falling back to Python orchestrator.")
            return False
    except FileNotFoundError:
        print("[Bridge] Node tooling (npx/tsx) not found. Falling back to Python orchestrator.")
        return False


def main():
    """
    Main launcher for the AI agent. It must be run from the project's root directory.
    Historically, this created a temporary copy and executed scripts/run_local_agent.py in it.

    Now deprecated: We attempt to bridge to the Node CLI (TypeScript implementation) first.
    If bridging is disabled or fails, we run the legacy Python flow to avoid blocking users.
    """
    parser = argparse.ArgumentParser(description="Launcher for the autonomous AI agent (deprecated Python path).")
    parser.add_argument("--model", type=str, default="gpt-4-turbo-preview", help="LLM model name (legacy path only).")
    parser.add_argument("--agent", type=str, required=False, choices=['developer', 'tester', 'planner', 'contexter', 'speccer'], help="Agent persona (legacy path only).")
    parser.add_argument("--task", type=str, help="Optional: Specify a task ID to work on.")
    parser.add_argument("--project-dir", type=str, help="Optional: Target child project directory.")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent

    print(DEPRECATION_BANNER)

    # Try to bridge to the Node CLI first
    bridged = try_bridge_to_node(project_root, args.task, args.project_dir)
    if bridged:
        return

    # Legacy fallback: copy to temp workspace and invoke the old orchestrator
    with tempfile.TemporaryDirectory() as temp_dir_str:
        temp_dir = Path(temp_dir_str)
        workspace_path = temp_dir / "workspace"

        print(f"Copying repository from '{project_root}' to temporary workspace: '{workspace_path}'")

        try:
            shutil.copytree(project_root, workspace_path, ignore=IGNORE_PATTERNS)
        except Exception as e:
            print(f"FATAL: Failed to copy repository to temporary directory: {e}")
            print("\n--- Full Stack Trace ---")
            traceback.print_exc()
            print("------------------------\n")
            return

        orchestrator_script_path = workspace_path / "scripts" / "run_local_agent.py"

        command = [
            "python3",
            str(orchestrator_script_path),
        ]
        # Legacy-only flags
        if args.agent:
            command.extend(["--agent", args.agent])
        if args.model:
            command.extend(["--model", args.model])
        if args.task:
            command.extend(["--task", str(args.task)])
        if args.project_dir:
            project_dir = workspace_path / args.project_dir
            command.extend(["--project-dir", str(project_dir)])

        print(f"Executing legacy orchestrator: {' '.join(command)}")

        try:
            subprocess.run(command, cwd=workspace_path, check=True)
        except subprocess.CalledProcessError as e:
            print(f"\n--- An error occurred while running the agent orchestrator: {e} ---")
            print("\n--- Full Stack Trace ---")
            traceback.print_exc()
            print("------------------------\n")
        except KeyboardInterrupt:
            print("\n--- Agent run interrupted by user. ---")

    print("\n--- Agent run finished. Temporary directory cleaned up. ---")

if __name__ == "__main__":
    main()
