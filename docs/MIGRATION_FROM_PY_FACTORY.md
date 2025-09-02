# Migration Guide: Python Factory -> TypeScript factory-ts

This guide explains how to migrate from the legacy Python-based Factory script to the new TypeScript library (factory-ts) used by Overseer and the Node CLI bridge.

## TL;DR

- Use Overseer (Electron app) to run agents with an integrated review UI.
- Or, use the Node CLI bridge (scripts/runAgent.ts) to launch runs and stream JSONL events to stdout.
- Project and task schemas remain the same: projects/<id>.json configs and per-project tasks under that project's folder.

## Key Differences

- Python: Invoked via a console script; applied file changes directly (often relying on external git tooling for review).
- TypeScript: Library + CLI; proposes changes in a sandbox, emits diffs, and integrates git commits on acceptance. Overseer provides an integrated review UI.
- Observability: Rich, structured events (progress, usage, errors, diffs, commits) and a persistent HistoryStore (SQLite) for runs.
- Shareability: Export/import full run archives (artifacts module).

## Project & Task Schema

- The TS orchestrator consumes the same project configs found in projects/*.json.
- Tasks live under the child project's folder (tasks/{id}/task.json). Features are defined within task.json.
- If you have existing projects configured for the Python script, no schema changes are required.

## Installing and Running the TS CLI

Prerequisites: Node 18+, npm or pnpm.

1) Install dependencies:
- pnpm install (or npm install)

2) Run the CLI directly (ts-node/tsx) or via a dev script. Example with tsx:
- npx tsx scripts/runAgent.ts \
  --project-id my-project \
  --project-root ../my-project \
  --task-id 7 \
  --feature-id 7.2 \
  --llm-config '{"provider":"openai","model":"gpt-4o-mini","apiKeyEnv":"OPENAI_API_KEY","temperature":0.2}' \
  --budget 10 \
  --db-path ./factory.history.sqlite

See docs/RUN_AGENT_CLI.md for the full argument list.

Output: One JSON event per line (JSONL). Each event conforms to packages/factory-ts/src/events/types.ts (RunEvent).

## Mapping Python Arguments to TS CLI

- project path (Python) -> --project-root (TS)
- project ID (if applicable) -> --project-id (TS)
- task id -> --task-id (TS)
- feature id -> --feature-id (TS)
- LLM config (env vars, provider/model) -> --llm-config (TS JSON string or path to JSON)
- budget (USD) -> --budget (TS)
- history DB path (optional) -> --db-path (TS)

Examples:
- Python (legacy):
  - python3 run_local_agent.py --project /path/to/proj --task 7 --feature 7.2 --model gpt-4 --budget 10
- TypeScript (CLI):
  - npx tsx scripts/runAgent.ts --project-root /path/to/proj --task-id 7 --feature-id 7.2 --llm-config '{"provider":"openai","model":"gpt-4o-mini","apiKeyEnv":"OPENAI_API_KEY"}' --budget 10

## LLMConfigs: Reuse and Mapping

The TS orchestrator accepts a serializable LLM config. You can reuse your existing provider+model choices from the Python setup by expressing them as JSON.

- OpenAI example:
```json
{
  "provider": "openai",
  "model": "gpt-4o-mini",
  "apiKeyEnv": "OPENAI_API_KEY",
  "temperature": 0.2,
  "maxTokens": 4096
}
```
- Anthropic example:
```json
{
  "provider": "anthropic",
  "model": "claude-3-5-sonnet",
  "apiKeyEnv": "ANTHROPIC_API_KEY",
  "temperature": 0.2
}
```

Notes:
- apiKeyEnv should point to the environment variable holding the API key. The CLI and Overseer will read it from process.env.
- Additional provider-specific fields can be included as needed (e.g., baseUrl, organization, topP).

## Usage, Budgets, and Cost Tracking

- The orchestrator emits run/usage events with token counts and cost estimates.
- If budget is set (e.g., --budget 10), a run/budget-exceeded event is emitted when reached.
- Use --db-path to persist history; Overseer uses the same HistoryStore under the hood.

## Reviewing and Applying Changes

- The CLI and Overseer both receive file/proposal and file/diff events.
- Overseer provides UI to accept/reject all/files. Accepted changes are committed on a feature branch (git/commit event emitted).
- From the CLI, you can implement a small script to listen for file/diff and hit a local service exposing reviewService (or rely on Overseer).

## Exporting and Sharing Runs

- Use the artifacts module to export a redacted archive (v1) for a completed or in-progress run. Archives can include optional file snapshots with size limits.

## Known Differences / Tips

- The TS orchestrator stages changes in a sandbox overlay; nothing touches your working tree until you accept.
- Event payloads are IPC-serializable JSON—avoid relying on Python-structured logs.
- For long-running tasks, prefer Overseer for an interactive experience. The CLI is best for automation and debugging.

## Next Steps

- Integrate Overseer: see docs/OVERSEER_INTEGRATION.md.
- Learn the event shapes and library APIs: see docs/FACTORY_TS_OVERVIEW.md.
- CLI reference: see docs/RUN_AGENT_CLI.md.
