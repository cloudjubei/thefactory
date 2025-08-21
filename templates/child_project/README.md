# {{PROJECT_NAME}}

This repository is a child project managed by a parent specification project. It is intended to be included as a Git submodule under the parent repository's `projects/` directory (e.g., `projects/{{PROJECT_NAME}}`).

## Overview
- Purpose: Describe the problem domain and goals for {{PROJECT_NAME}}.
- Ownership: This child project owns its implementation details while aligning with the parent project's specifications.
- Linkage: Managed as a Git submodule under the parent project.

## Getting Started
1. Clone this repository (standalone or via parent project's submodule).
2. Install any required tooling for your chosen stack (document below).
3. Read `spec.md` to understand scope, requirements, and acceptance criteria.

## Repository Structure
- `README.md`: High-level overview and usage guidelines.
- `spec.md`: Project specification (purpose, scope, requirements, milestones).
- `src/` (suggested): Source code lives here.
- `tests/` (suggested): Tests live here.

You may add or adjust directories as needed for your stack. Keep `spec.md` up to date.

## Development Workflow
- Work from issues or milestones derived from `spec.md`.
- Keep changes small and traceable back to the specification.
- Update `spec.md` when the scope or acceptance criteria evolve.

## Submodule Link to Parent
If this repository is included as a submodule under a parent project:
- Path in parent: `projects/{{PROJECT_NAME}}`
- Synchronization: Parent updates may require submodule updates. Use `git submodule update --remote --merge` as appropriate.
- Independence: This repo can also be cloned and developed independently.

## Contributing
- Open issues for questions or changes to scope.
- Use feature branches and PRs.
- Follow any coding standards agreed upon for this project.

## License
Specify the license for {{PROJECT_NAME}} here.
