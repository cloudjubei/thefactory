# Projects Guide: Managing child projects under projects/ with Git submodules

This guide explains how the projects/ folder is used to control child projects and how those projects are orchestrated by the TypeScript library (factory-ts) and Overseer.

## Overview
- The projects/ directory contains child project config files.
- Each child project is typically a separate Git repository hosted elsewhere (added as a submodule or referenced by path).
- The factory-ts orchestrator (used by Overseer and the Node CLI) reads these configs to locate project roots and their tasks.

Typical layout:
- projects/<name>.json: a config file containing relevant information about the child project.

Minimal config fields (ProjectSpec):
- id: string (unique project id; also used as the filename without extension)
- name: string (display name)
- path: string (path to the child project's root, relative to the superproject root)
- description?: string
- tags?: string[]

Example projects/my-awesome-project.json:
```json
{
  "id": "my-awesome-project",
  "name": "My Awesome Project",
  "path": "../my-awesome-project",
  "description": "A new awesome project.",
  "tags": ["web", "examples"]
}
```

Tasks are discovered under the child project's tasks/ directory, e.g., ../my-awesome-project/tasks/{id}/task.json.

## Creating a New Child Project Using child_project_utils.py

To automate the creation and addition of a new child project, you can use the existing Python helper script `scripts/child_project_utils.py`. This script creates the project directory structure, initializes a local git repository, adds initial files (like README.md, .gitignore, .env, docs/FILE_ORGANISATION.md, and an initial task), commits them, and adds the project's configuration json under /projects.

Step-by-step:
1. Ensure you are in the root directory of the superproject and have Python and Git installed.
2. Run the script with the project name and optional arguments:
   - Example: `python3 scripts/child_project_utils.py my-awesome-project --description "A new awesome project." --path ../my-awesome-project`
   - Optional: `--repo-url git@github.com:user/my-repo.git` to set a remote origin.
   - Optional: `--task-id 7` to seed from the superproject's tasks/7 (see below).
   - Optional: `--dry-run` to simulate without making changes.
3. Commit the config file addition to the superproject:
   - `git add projects/my-awesome-project.json`
   - `git commit -m "Add new child project my-awesome-project"`
4. If a remote URL was provided, navigate to the child project and push:
   - `cd ../my-awesome-project && git push origin main && cd -`

### Seeding a child project from an existing task with --task-id

You can seed the new child project with an existing task from the superproject using the `--task-id` option.

- What it does:
  - Copies the superproject's `tasks/{id}/` directory into the child project as `tasks/1/`.
  - Rewrites the `task.json` IDs so that the top-level `id` becomes `1` and features are remapped accordingly.
- Example invocation:
  - `python3 scripts/child_project_utils.py my-seeded-project --path ../my-seeded-project --task-id 7`
- Requirements and notes:
  - The source directory `tasks/7/` must exist in the superproject.
  - After creation, the child project will contain `tasks/1/task.json` with IDs rewritten to start at `1`.

## Running Agents for a Child Project

You have two options:

1) Overseer (recommended):
- Overseer uses the factory-ts library to launch runs, display progress/usage, and show diffs for acceptance.
- See docs/OVERSEER_INTEGRATION.md for how events are bridged and consumed.

2) Node CLI Bridge (for automation and debugging):
- Use `scripts/runAgent.ts` to launch a run and stream JSONL events.
- Basic usage:
  - `npx tsx scripts/runAgent.ts --project-id my-awesome-project --project-root ../my-awesome-project --task-id 7 --feature-id 7.2 --llm-config '{"provider":"openai","model":"gpt-4o-mini","apiKeyEnv":"OPENAI_API_KEY"}' --budget 10`
- See docs/RUN_AGENT_CLI.md for the full argument list.

## Notes and Schema Clarifications

- The config file follows the ProjectSpec used by both Overseer and the TS orchestrator. At minimum, include `id`, `name`, and `path`.
- Task definitions within the child project keep their existing schema (tasks/{id}/task.json). No changes are required when migrating to the TS orchestrator.
- The TS orchestrator proposes file changes in a sandbox; acceptance actions will create commits on a feature branch via the git service. This allows integrated accept/reject flows within Overseer.

## Managing child projects
A child project remains managed as long as its config .json is under `projects/<name>.json`. Remove or rename the file to stop managing it in the superproject.
