# Local App Project Specification

## References
- docs/SPEC.md
- docs/TASK_FORMAT.md
- docs/PLAN_SPECIFICATION.md
- docs/FEATURE_FORMAT.md
- docs/FILE_ORGANISATION.md
- docs/TESTING.md

## Problem Statement
We need a dedicated, local application to manage this project: view tasks, inspect progress, and interact with agents. While development today commonly uses editors like VSCode, a purpose-built local app can present an opinionated interface aligned with this project's specification-first methodology and tool-based agent flow.

## Scope
This document provides the specification and step-by-step guidance to create a separate "Local App" repository that follows the same principles as this project. It defines:
- The initial repository bootstrap and structure
- MVP goals and success criteria
- Architecture options and a recommended baseline
- Integration methods with this project's repository
- An initial task backlog for the new repository

Out of scope for this task: implementing the app itself here. The app will be built in its own repo following this spec.

## Constraints
- Third-party independence by default: Prefer self-hosted or local-first solutions. Use third-party services only where justified and documented via tasks.
- Cross-platform where reasonably achievable (macOS, Windows, Linux). If constraints arise, document them.
- Offline-capable for core browsing of a locally-available repository.
- Safe execution: no arbitrary system commands from the UI without explicit user action.

## MVP Success Criteria
The Local App MVP is considered successful when:
1. A user can point the app at a repository containing tasks/TASKS.md and see a parsed, navigable list of tasks with statuses and details.
2. Selecting a task shows its metadata (ID, status, Action, Acceptance, Notes) and links to its plan file if present.
3. The app provides a button or flow to open relevant spec files for quick reference.
4. The app can refresh its view when the underlying repo changes (manual refresh acceptable for MVP).
5. The repository is structured according to docs/FILE_ORGANISATION.md adapted for the Local App project.

## Architecture and Technology Options
Options (choose one via a decision task in the Local App repo):
- Tauri + React/TypeScript
  Pros: Lightweight, secure, good performance, cross-platform. Cons: Some native toolchain setup.
- Electron + React/TypeScript
  Pros: Mature ecosystem. Cons: Larger runtime footprint.
- Pure Python + PySide/PyQt
  Pros: Single-language, strong tooling. Cons: Packaging complexity, larger binaries.
- Local Web App (Flask/FastAPI backend + local web UI)
  Pros: Familiar web stack. Cons: Requires running a local server process.

Recommended starting point: Tauri + React/TypeScript for a lean cross-platform desktop app with good performance and local file access.

## Repository Bootstrap
Follow these steps to create the new repository (e.g., "local-app"):
1. Create a new git repository and initialize the structure:
   - .github/ (optional workflows later)
   - docs/
   - scripts/
   - src/
   - tasks/
   - tests/
   - .gitignore, README.md, requirements.txt or package.json (depending on stack)
2. Seed core documentation by referencing or copying baseline specs from this project:
   - docs/SPEC.md
   - docs/TASK_FORMAT.md
   - docs/PLAN_SPECIFICATION.md
   - docs/FEATURE_FORMAT.md
   - docs/FILE_ORGANISATION.md (tuned for the app)
   - docs/TESTING.md
3. Create tasks/TASKS.md with an initial backlog (see Initial Task Backlog below).
4. If using a desktop framework (e.g., Tauri + React):
   - Initialize the app scaffold (e.g., `pnpm create tauri-app` or equivalent)
   - Create UI route(s): Tasks list, Task detail view
   - Add a file reader module to load tasks/TASKS.md and optional plan files
5. Add basic tests in tasks/{id}/tests to verify outputs (e.g., that docs exist and core parsing works for a sample tasks file).

## Data Model (MVP)
- Task
  - id: int
  - status: one of [+,-,~,?,/,=]
  - title: string
  - action: string
  - acceptance: string
  - notes: optional string
  - plan_path: derived (tasks/{id}/plan_{id}.md if exists)

## Parsing Rules
- Parse tasks/TASKS.md according to docs/TASK_FORMAT.md.
- Preserve ordering and display the exact status symbol.
- Link the plan file when present.

## Integration with This Project
The app should support multiple data sources:
- Local filesystem: User selects a local clone path; the app reads tasks/TASKS.md and related files directly.
- GitHub remote (optional later): Fetch files via the GitHub API using a user-provided token. This should be added via a dedicated task with security notes.

## Security and Privacy
- Store tokens (if any) securely using OS keychain or encrypted storage.
- Do not transmit repository content externally unless the user explicitly opts in.

## User Flows (MVP)
1. Select repository (folder picker)
2. Load tasks
3. View list with status filters
4. Click a task to see details and open plan/spec links
5. Refresh data

## Initial Task Backlog (for the Local App repository)
1) - Project scaffolding
   Action: Initialize repo structure and baseline docs as per this spec.
   Acceptance: Repo has the documented directories and core docs in place.

2) - Task parser
   Action: Implement a parser for tasks/TASKS.md that respects docs/TASK_FORMAT.md.
   Acceptance: Given a sample TASKS.md, the parser returns a structured list of tasks.

3) - UI: Tasks list view
   Action: Display tasks with status badges and filters.
   Acceptance: User sees all tasks and can filter by status symbol.

4) - UI: Task detail view
   Action: Show task fields and link to plan file.
   Acceptance: Selecting a task shows Action, Acceptance, Notes, and plan link if present.

5) - Repository selection
   Action: Implement a folder picker and persist last used path.
   Acceptance: User can change the repository and the app refreshes tasks.

6) - Testing setup
   Action: Establish minimal testing per docs/TESTING.md equivalent for the app.
   Acceptance: Tests exist for the parser and basic UI sanity (where applicable).

7) - Optional: GitHub API integration
   Action: Fetch tasks from remote via token.
   Acceptance: With a valid token, app loads tasks without a local clone.

## Roadmap
- Agent orchestration integration (launch tasks via orchestrator)
- Multi-repo support and workspaces
- Progress metrics and timelines
- Notifications for changes in tasks

## Notes
- This project mirrors the principles and workflow of this repository. Plans and features should follow docs/PLAN_SPECIFICATION.md and docs/FEATURE_FORMAT.md. All features must have tests per docs/TESTING.md.
