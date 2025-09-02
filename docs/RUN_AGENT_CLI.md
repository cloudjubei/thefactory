# Run Agent CLI (TypeScript)

This CLI acts as a backward-compatible bridge to launch agents (replacing the Python entrypoint). It streams run events as JSONL to stdout, so Overseer or other tools can observe progress and outcomes.

Usage
- Install deps (once):
  - npm install
- Run:
  - npm run run:agent -- \
    --project-id child-project-1 \
    --task-id 42 \
    --feature-id 1 \
    --llm-config ./overseer_llm.json \
    --budget 5 \
    --db-path ./.thefactory/history.sqlite \
    --project-root .

Arguments
- --project-id (required): ID of the project (matches projects/{project_id}.json in Overseer).
- --task-id (required): Task ID within the project to run.
- --feature-id (optional): Specific feature within the task to run.
- --llm-config (optional): Either a path to a JSON file or inline JSON string. If not provided, the library may use defaults.
- --budget (optional): Numeric dollar budget (e.g., 5 for $5). Enforced by the telemetry module where supported.
- --db-path (optional): SQLite database path for run history; if omitted, the library may use defaults.
- --project-root (optional): Root of the target project workspace. Defaults to current working directory.

Output
- JSON Lines on stdout representing lifecycle and orchestrator events.
- Example:
  {"type":"cli/started","ts":"...","payload":{...}}
  {"type":"run/progress","ts":"...","payload":{...}}
  {"type":"run/completed","ts":"...","payload":{"status":"success"}}

Exit codes
- 0: success
- 1: run error
- 2: invalid/missing arguments
- 3: orchestrator import error

Signals
- SIGINT (Ctrl+C) cancels the running agent via AbortController and emits a run/aborting event.

Notes
- The CLI attempts to dynamically import the orchestrator from packages/factory-ts. It tries common dist and src paths, as well as a package import. Adjust paths as needed if your layout differs.
