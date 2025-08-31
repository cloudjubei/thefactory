#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys
import json
import shutil
from pathlib import Path
import uuid
from dotenv import load_dotenv, find_dotenv, set_key

load_dotenv()

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

EXAMPLE_TASK_JSON_PATH = Path("docs/tasks/task_example.json")

# --- Helper Functions ---

def run_command(command, cwd=None, dry_run=False, allow_fail=False):
    """Runs a command and handles dry-run mode."""
    command_str = " ".join(command)
    print(f"[{'DRY RUN' if dry_run else 'EXEC'}] CWD: {cwd or '.'} | CMD: {command_str}")
    if not dry_run:
        try:
            result = subprocess.run(
                command,
                cwd=cwd,
                check=not allow_fail,
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
            if not allow_fail:
                sys.exit(1)
            return e
    return None

def check_git_installed():
    """Checks if git is installed."""
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("Error: 'git' command not found. Please install Git and ensure it's in your PATH.", file=sys.stderr)
        sys.exit(1)


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Generate a new child project structure under projects/, initialize it as a git repository, "
            "and add it as a submodule to the parent repository."
        ),
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Examples:
  # Create a new project named 'my-awesome-feature' in the default 'projects/' directory
  python3 scripts/child_project_utils.py my-awesome-feature --description "A new awesome feature."

  # Create a project with a remote repository URL (SSH)
  python3 scripts/child_project_utils.py my-new-service --repo-url git@github.com:user/my-new-service.git

  # Seed the child project with an existing task folder (tasks/{id}/) rewritten to tasks/{newId}
  python3 scripts/child_project_utils.py my-seeded-proj --task-id 7

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
        "--task-id",
        type=int,
        help=(
            "Seed the child project's tasks/1/ by copying the superproject's tasks/{id}/ folder and "
            "rewriting task.json ids to start with 1."
        )
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the planned actions without executing them."
    )

    args = parser.parse_args()

    parent_env_path = Path(find_dotenv()) if find_dotenv() else None

    # --- 1. Path validation and setup ---
    base_path = Path(args.path)
    project_path = base_path / args.project_name
    env_path = project_path / ".env"
    tasks_dir = project_path / "tasks"
    tasks_one_dir = tasks_dir / "1"
    readme_path = project_path / "README.md"
    gitignore_path = project_path / ".gitignore"
    task_json_path = tasks_one_dir / "task.json"

    print(f"Target project path: {project_path.resolve()}")

    if project_path.exists():
        print(f"Error: Directory '{project_path}' already exists. Please choose a different project name or path.", file=sys.stderr)
        sys.exit(1)

    if not args.dry_run:
        check_git_installed()

    # --- 2. Create project structure ---
    if not args.dry_run:
        try:
            base_path.mkdir(parents=True, exist_ok=True)
            project_path.mkdir(exist_ok=False)
            if args.repo_url:
                clone_result = run_command(["git", "clone", args.repo_url, "."], cwd=project_path, allow_fail=True)
                if clone_result.returncode != 0:
                    print("Warning: Clone failed. Initializing local repository instead.", file=sys.stderr)
                    run_command(["git", "init"], cwd=project_path, dry_run=False)
            else:
                run_command(["git", "init"], cwd=project_path, dry_run=False)

            tasks_dir.mkdir(exist_ok=True)

            # README and .gitignore
            readme_content = f"# {args.project_name}\n\n{args.description}\n"
            readme_path.write_text(readme_content, encoding='utf-8')
            gitignore_path.write_text(GITIGNORE_TEMPLATE.strip() + "\n", encoding='utf-8')

            # Handle .env file
            if parent_env_path and parent_env_path.exists():
                try:
                    shutil.copy(parent_env_path, env_path)
                except Exception as e:
                    print(f"Error copying .env file: {e}", file=sys.stderr)
                    sys.exit(1)
            else:
                default_content = f'GIT_REPO_URL=""\nGIT_USER_NAME="{os.getenv("GIT_USER_NAME", "")}"\nGIT_USER_EMAIL="{os.getenv("GIT_USER_EMAIL", "")}"\nGIT_PAT="{os.getenv("GIT_PAT", "")}"\n'
                env_path.write_text(default_content, encoding='utf-8')
                print("Warning: No parent .env found. Created default .env with GIT_REPO_URL=\"\" and other Git settings from environment.", file=sys.stderr)

            if args.repo_url:
                set_key(str(env_path), "GIT_REPO_URL", args.repo_url)

            if args.task_id is not None:
                src_task_dir = Path("tasks") / args.task_id
                if not src_task_dir.exists() or not src_task_dir.is_dir():
                    print(f"Error: Source task directory '{src_task_dir}' does not exist.", file=sys.stderr)
                    sys.exit(1)
                shutil.copytree(src_task_dir, tasks_one_dir)
                if not task_json_path.exists():
                    print(f"Error: Expected '{task_json_path}' to exist after copying, but it was not found.", file=sys.stderr)
                    sys.exit(1)
                data = load_json(task_json_path)
                data["id"] = uuid.uuid4() # new id to make sure no clashes between projects
                save_json(task_json_path, data)
            else:
                tasks_one_dir.mkdir(exist_ok=True)
                if not EXAMPLE_TASK_JSON_PATH.exists():
                    print(f"Error: Example task JSON not found at '{EXAMPLE_TASK_JSON_PATH}'.", file=sys.stderr)
                    sys.exit(1)
                example_data = load_json(EXAMPLE_TASK_JSON_PATH)
                save_json(task_json_path, example_data)

            print("\nProject structure created successfully.")
        except Exception as e:
            print(f"Error creating project structure: {e}", file=sys.stderr)
            sys.exit(1)

    # --- 3. Initialize child git repository ---
    if not args.dry_run:
        run_command(["git", "add", "."], cwd=project_path, dry_run=False)
        run_command(["git", "commit", "-m", "Initial commit from scaffolding script"], cwd=project_path, dry_run=False)
        if args.repo_url:
            run_command(["git", "push", "origin", "main"], cwd=project_path, dry_run=False, allow_fail=True)

    # --- 4. Add as submodule to parent repository ---
    if not args.dry_run:
        relative_project_path = os.path.relpath(project_path.resolve(), Path.cwd().resolve())
        submodule_url = args.repo_url if args.repo_url else f"./{relative_project_path}"
        run_command(["git", "submodule", "add", "-b", "main", submodule_url, relative_project_path], dry_run=False, allow_fail=True)

        print("\nACTION REQUIRED: Please commit the new submodule to the parent repository:")
        print(f"  git add .gitmodules {relative_project_path}")
        print(f'  git commit -m "feat: Add submodule for project {args.project_name}"')

    sys.exit(0)

if __name__ == "__main__":
    main()
