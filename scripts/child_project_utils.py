#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys
from pathlib import Path

# --- Constants ---
DEFAULT_PROJECTS_PATH = "projects"
GITIGNORE_TEMPLATE = """
# Python
__pycache__/
*.py[cod]
*$py.class
.Python
env/
venv/
ENV/
.env
.venv

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
package-lock.json
yarn.lock

# Editor/OS files
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Temporary files
*.tmp
*.bak
*.log
"""
INITIAL_TASK_CONTENT = """
# Task 0: Initial Task

This is a placeholder task to get you started. Plan your feature here.
"""

# --- Helper Functions ---

def run_command(command, cwd=None, dry_run=False):
    """Runs a command and handles dry-run mode."""
    command_str = " ".join(command)
    print(f"[{'DRY RUN' if dry_run else 'EXEC'}] CWD: {cwd or '.'} | CMD: {command_str}")
    if not dry_run:
        try:
            result = subprocess.run(
                command,
                cwd=cwd,
                check=True,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            if result.stdout:
                print(result.stdout.strip())
            if result.stderr:
                print(result.stderr.strip(), file=sys.stderr)
            return result
        except FileNotFoundError:
            print(f"Error: Command '{command[0]}' not found. Is it in your PATH?", file=sys.stderr)
            sys.exit(1)
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {command_str}", file=sys.stderr)
            print(f"Return code: {e.returncode}", file=sys.stderr)
            print(f"Output:\n{e.stdout}\n{e.stderr}", file=sys.stderr)
            sys.exit(1)
    return None

def check_git_installed():
    """Checks if git is installed."""
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("Error: 'git' command not found. Please install Git and ensure it's in your PATH.", file=sys.stderr)
        sys.exit(1)

def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Generate a new child project structure, initialize it as a git repository, and add it as a submodule.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Examples:
  # Create a new project named 'my-awesome-feature' in the default 'projects/' directory
  python3 scripts/child_project_utils.py my-awesome-feature --description \"A new awesome feature.\"

  # Create a project with a remote repository URL
  python3 scripts/child_project_utils.py my-new-service --repo-url git@github.com:user/my-new-service.git

  # Perform a dry run to see what would happen without making changes
  python3 scripts/child_project_utils.py my-test-project --dry-run
"""
    )
    parser.add_argument(
        "project_name",
        help="The name of the new child project. This will be used for the directory name."
    )
    parser.add_argument(
        "-d", "--description",
        default="A new child project.",
        help="A short description for the project's README.md."
    )
    parser.add_argument(
        "-r", "--repo-url",
        help="The remote Git repository URL to be set as 'origin'."
    )
    parser.add_argument(
        "-p", "--path",
        default=DEFAULT_PROJECTS_PATH,
        help=f"The parent directory for the new project. Defaults to '{DEFAULT_PROJECTS_PATH}/'."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the planned actions without executing them."
    )

    args = parser.parse_args()

    if not args.dry_run:
        check_git_installed()
    
    # --- 1. Path validation and setup ---
    base_path = Path(args.path)
    project_path = base_path / args.project_name
    
    print(f"Target project path: {project_path.resolve()}")

    if project_path.exists():
        print(f"Error: Directory '{project_path}' already exists. Please choose a different project name or path.", file=sys.stderr)
        sys.exit(1)

    # --- 2. Create project structure ---
    tasks_dir = project_path / "tasks"
    readme_path = project_path / "README.md"
    gitignore_path = project_path / ".gitignore"
    initial_task_path = tasks_dir / "000_initial_task.md"
    
    print("\n--- Planning filesystem changes ---")
    actions = [
        f"Create directory: {base_path}",
        f"Create directory: {project_path}",
        f"Create directory: {tasks_dir}",
        f"Create file: {readme_path}",
        f"Create file: {gitignore_path}",
        f"Create file: {initial_task_path}",
    ]
    for action in actions:
        print(action)
    
    if not args.dry_run:
        try:
            base_path.mkdir(parents=True, exist_ok=True)
            project_path.mkdir(exist_ok=False)
            tasks_dir.mkdir()
            
            readme_content = f"# {args.project_name}\n\n{args.description}\n"
            readme_path.write_text(readme_content, encoding='utf-8')
            gitignore_path.write_text(GITIGNORE_TEMPLATE.strip(), encoding='utf-8')
            initial_task_path.write_text(INITIAL_TASK_CONTENT.strip(), encoding='utf-8')
            
            print("\nProject structure created successfully.")
        except Exception as e:
            print(f"Error creating project structure: {e}", file=sys.stderr)
            sys.exit(1)

    # --- 3. Initialize child git repository ---
    print("\n--- Planning child git repository initialization ---")
    run_command(["git", "init"], cwd=project_path, dry_run=args.dry_run)
    if args.repo_url:
        run_command(["git", "remote", "add", "origin", args.repo_url], cwd=project_path, dry_run=args.dry_run)
    run_command(["git", "add", "."], cwd=project_path, dry_run=args.dry_run)
    run_command(["git", "commit", "-m", "Initial commit from scaffolding script"], cwd=project_path, dry_run=args.dry_run)

    # --- 4. Add as submodule to parent repository ---
    print("\n--- Planning submodule addition to parent repository ---")
    # For git, paths must be relative to the repo root (current directory).
    # Resolve the path to handle cases where args.path might be ../etc
    relative_project_path = os.path.relpath(project_path.resolve(), Path.cwd().resolve())

    submodule_url = args.repo_url if args.repo_url else f"./{relative_project_path}"
    run_command(["git", "submodule", "add", submodule_url, relative_project_path], dry_run=args.dry_run)
    
    print(f"\nSuccessfully {'planned' if args.dry_run else 'created'} project '{args.project_name}'.")
    if not args.dry_run:
        print("\nACTION REQUIRED: Please commit the new submodule to the parent repository:")
        print(f"  git add .gitmodules {relative_project_path}")
        print(f'  git commit -m "feat: Add submodule for project {args.project_name}"')
        
    sys.exit(0)

if __name__ == "__main__":
    main()
