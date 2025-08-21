# Child Projects Specification

This document defines the structure, purpose, and management of child projects associated with this parent repository.

## Purpose and Overview
- Child projects encapsulate focused, independently-cloneable workstreams driven by this parent project’s specifications.
- The parent repository maintains a curated set of child projects as Git submodules, ensuring consistent versions and easy updates.

## Location in Parent Repository
- All child projects are located under the `projects/` directory in this repository.
- Each child project is tracked as a Git submodule at a path like `projects/<project_name>`.

## Submodule Management
- Child projects are included in the parent repo using Git submodules. This means the parent repository stores a reference (a specific commit) to each child project rather than its full source.
- Typical operations:
  - Add a new child project: `git submodule add <repo-url> projects/<project_name>`
  - Initialize submodules: `git submodule init`
  - Update submodules to referenced commits: `git submodule update --recursive`
  - Update a submodule to a new commit (within `projects/<project_name>`), commit in the child repo, then commit the new submodule pointer in the parent repo.
- Benefits:
  - Clear version pinning of each child project.
  - Controlled updates: the parent advances the submodule pointer after validation.

## Expected Child Project Repository Structure
A child project repository should start with the following minimal structure:

```
<child_project_root>/
  README.md        # Overview, goals, setup, usage
  spec.md          # The child project’s own specification and acceptance criteria
  .gitignore       # Ignore patterns suitable for the technology used
  (optional) src/  # Source code or implementation area
  (optional) docs/ # Additional documentation
```

- Required files:
  - `README.md`: Introduces the project and basic usage.
  - `spec.md`: Defines the project’s scope, requirements, and acceptance criteria.
  - `.gitignore`: Standard ignore rules for the project’s language/runtime.

## Relationship to the Parent Project
- The parent project defines specifications and high-level direction. Child projects implement those specifications and may evolve independently.
- The parent tracks each child via a submodule under `projects/`. When a child project is updated and validated, the parent updates the submodule reference and commits the change.
- Child projects can also be cloned and developed independently of this parent. However, integration with the parent is governed by submodule updates.

## Typical Workflow
1. Create a new child repository (or use an existing one) with the boilerplate files (`README.md`, `spec.md`, `.gitignore`).
2. Add it to the parent as a submodule under `projects/<project_name>`.
3. Develop features in the child project, commit and push to its own remote.
4. In the parent repo, update the submodule pointer to the new validated commit and commit the change.

## Notes and Conventions
- Keep child project READMEs and specs up-to-date to ensure maintainability and clarity.
- Ensure `projects/` remains the canonical location for submodules in this parent repository.
- Avoid embedding large binaries directly in child repos; prefer artifact registries when needed.
