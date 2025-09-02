# TheFactory (Monorepo)

Primary orchestrator implementation: TypeScript (packages/factory-ts), consumable by Overseer (Electron app) and via a Node CLI bridge.

Python entrypoints are deprecated and will be removed after the transition period. They now print a deprecation notice and will attempt to delegate to the Node CLI when available. If the Node CLI is not available, the Python flow will continue to work to avoid blocking users.

Quick start (TypeScript/Node):
- Run the Node CLI (no build step needed):
  npx -y tsx scripts/runAgent.ts --project-root . --task-id 1

- See docs/RUN_AGENT_CLI.md for full argument reference.

Overseer integration:
- The TS library is in packages/factory-ts and exposes orchestration APIs and IPC-friendly events. See docs/OVERSEER_INTEGRATION.md and examples/overseer-integration/.

Deprecation details:
- Python entrypoints (run.py and scripts/run_local_agent.py) print a deprecation banner on startup.
- By default, they attempt to shell out to the Node CLI using npx tsx scripts/runAgent.ts with minimal arguments.
- If Node or npx is not available, or delegation fails, the Python flow continues.

Environment flags for the bridge:
- FACTORY_FORCE_PYTHON=1: Do not bridge; always run the legacy Python flow.
- FACTORY_BRIDGE_TO_NODE=0: Disable auto-bridge (same effect as FACTORY_FORCE_PYTHON=1).
- FACTORY_NODE_CMD (optional): Override the Node CLI command (default: npx -y tsx scripts/runAgent.ts).

Notes:
- The Node CLI streams JSONL events compatible with packages/factory-ts/src/events/types.ts.
- Git integration and review flows are implemented in the TS library; Overseer presents diffs and allows accept/reject.
