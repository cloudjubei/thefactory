# Projects Guide: Managing child projects under projects/ with Git submodules

This guide explains how the projects/ folder is used to control child projects.
## Overview
- The projects/ directory contains child project configs.
- Each child project is a separate Git repository hosted elsewhere.

Typical layout:
- projects/<name>.json: a config file containing relevant information. The config file follows the `ProjectSpec` interface defined in `docs/tasks/task_format.py`.

## Creating a New Child Project Using child_project_utils.py

To automate the creation and addition of a new child project, use the `scripts/child_project_utils.py` script. This script creates the project directory structure, initializes a local git repository, adds initial files (like README.md, .gitignore, .env, docs/FILE_ORGANISATION.md, and an initial task), commits them, and adds the project's configuration json under /projects.

### Step-by-Step Guide to Using the Script

1. Ensure you are in the root directory of the main project and have Python and Git installed.
2. Run the script with the project name and optional arguments:
   - Example: `python3 scripts/child_project_utils.py my-awesome-project --description "A new awesome project." --path ../my-awesome-project`
   - Optional: `--repo-url git@github.com:user/my-repo.git` to set a remote origin.
   - Optional: `--task-id 7` to seed the child project from the superproject's tasks/7 (see details below).
   - Optional: `--dry-run` to simulate without making changes.
3. After the script completes, commit the config file addition to the superproject:
   - `git add projects/my-awesome-project.json`
   - `git commit -m "Add new child project my-awesome-project"`
4. If a remote URL was provided, navigate to the child project and push:
   - `cd ../my-awesome-project`
   - `git push origin main`
   - `cd -`

This sets up the child project. For manual addition or other operations, see the sections below.

### Seeding a child project from an existing task with --task-id

You can seed the new child project with an existing task from the superproject using the `--task-id` option.

- What it does:
  - Copies the superproject's `tasks/{id}/` directory into the child project as `tasks/1/`.
  - Rewrites the `task.json` IDs so that:
    - The top-level `id` becomes `1`.
    - Each feature's ID that originally looked like `X.suffix` becomes `1.suffix`.
- Example invocation:
  - `python3 scripts/child_project_utils.py my-seeded-project --path ../my-seeded-project --task-id 7`
- Requirements and notes:
  - The source directory `tasks/7/` must exist in the superproject.
  - After creation, the child project will contain `tasks/1/task.json` with IDs rewritten to start at `1`.

## Managing child projects
A child project is managed as long as its config .json is under projects/<name>
