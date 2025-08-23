# Projects Guide: Managing child projects under projects/ with Git submodules

This guide explains how the projects/ folder is used to host child projects as Git submodules, and provides end-to-end instructions for cloning, initializing, adding, updating, switching branches, removing submodules, plus common pitfalls, CI/CD notes, and troubleshooting tips.

## Overview
- The projects/ directory contains child projects, each tracked as a Git submodule.
- Each submodule is its own Git repository with independent history.
- The superproject (this repo) records only a pointer (a specific commit) to each submodule.
- Changes inside a submodule must be committed within that submodule, and then the superproject must commit the updated submodule pointer.

Typical layout:
- projects/<name>: a submodule checkout pointing to a specific commit of the child project.

## Creating a New Child Project Using child_project_utils.py

To automate the creation and addition of a new child project, use the `scripts/child_project_utils.py` script. This script creates the project directory structure, initializes a local git repository, adds initial files (like README.md, .gitignore, and an initial task), commits them, and adds the project as a git submodule in the main repository.

### Step-by-Step Guide to Using the Script

1. Ensure you are in the root directory of the main project and have Python and Git installed.

2. Run the script with the project name and optional arguments:
   - Example: `python3 scripts/child_project_utils.py my-awesome-feature --description "A new awesome feature."`
   - Optional: `--repo-url git@github.com:user/my-repo.git` to set a remote origin.
   - Optional: `--path projects` (default) to specify the parent directory.
   - Optional: `--dry-run` to simulate without making changes.

3. After the script completes, commit the submodule addition in the main project as prompted:
   - `git add .gitmodules projects/my-awesome-feature`
   - `git commit -m "Add new child project my-awesome-feature"`

4. If a remote URL was provided, navigate to the child project and push:
   - `cd projects/my-awesome-feature`
   - `git push origin main`
   - `cd -`

This sets up the child project linked via git submodules. For manual addition or other operations, see the sections below.

## Cloning with submodules
Recommended: clone with all submodules initialized and checked out in a single step.

- git clone --recurse-submodules <superproject_url>

If you already cloned without submodules, you can initialize and fetch them later:
- git submodule init
- git submodule update

Combined variant that works for both init and update, including nested submodules:
- git submodule update --init --recursive

Tip: Use git submodule status to see current submodule states and commits.

## Adding a new child project under projects/<name>
Add a submodule under projects/<name>. Choose the branch you want to track for updates.

Example (tracking main):
- git submodule add -b main <child_repo_url> projects/<name>

This creates/updates .gitmodules and adds a new entry in .git/config. After adding, you must commit both:
- git add .gitmodules projects/<name>
- git commit -m "Add submodule projects/<name> tracking main"

Notes:
- The -b <branch> option sets the branch you want to track for future updates via git submodule update --remote.
- Be consistent with authentication (SSH vs HTTPS). See Authentication below.

## Updating submodules to newer commits
There are two common ways to update:

1) From the superproject using the tracked branch
- git submodule update --remote projects/<name>
- Optionally, include nested submodules: git submodule update --remote --recursive
- Then commit the pointer bump in the superproject:
  - git add projects/<name>
  - git commit -m "Bump submodule projects/<name> to latest on tracked branch"

2) Inside the submodule directly
- cd projects/<name>
- git fetch
- git checkout <desired_branch_or_commit>
- git pull --ff-only (if on a branch)
- cd -
- git add projects/<name>
- git commit -m "Bump submodule projects/<name> to <new_commit>"

Bulk operations with foreach (useful when you have many submodules):
- git submodule foreach 'git status'
- git submodule foreach --recursive 'git fetch --all'
- git submodule foreach --recursive 'git pull --ff-only || true'
- git submodule foreach --recursive 'git checkout main || true'

Always remember: after updating submodule content, you must commit the new pointer in the superproject.

## Switching the tracked branch for a submodule
To change which branch a submodule tracks for git submodule update --remote:
- git config -f .gitmodules submodule.projects/<name>.branch <branch>
- git submodule sync --recursive
- git add .gitmodules
- git commit -m "Track <branch> for projects/<name>"

Then update to the latest on the new branch if desired:
- git submodule update --remote projects/<name>
- git add projects/<name>
- git commit -m "Bump projects/<name> to latest on <branch>"

## Removing a child project submodule
To fully remove a submodule and its metadata:
- git submodule deinit -f projects/<name>
- git rm -f projects/<name>
- rm -rf .git/modules/projects/<name>

This updates .gitmodules automatically or removes its entry. Commit the changes:
- git add .gitmodules || true
- git commit -m "Remove submodule projects/<name>"

## Authentication: SSH vs HTTPS
- Submodule URLs can be SSH (git@github.com:org/repo.git) or HTTPS (https://github.com/org/repo.git).
- Be consistent across your team and CI. Mixing SSH and HTTPS across submodules or between local and CI environments commonly causes auth prompts or failures.
- If changing URLs in .gitmodules, run git submodule sync --recursive to propagate changes to .git/config.
- Ensure CI has the correct credentials:
  - SSH: deploy keys/known_hosts configured.
  - HTTPS: tokens with required access scopes.

## CI/CD notes
To fetch submodules in automation:
- Preferred fresh checkout:
  - git clone --recurse-submodules <superproject_url>
- Or if repository already checked out:
  - git submodule update --init --recursive

If you change submodule URLs or branches, also run:
- git submodule sync --recursive

Ensure CI does not forget to initialize nested submodules if present.

## Troubleshooting
- See current submodule states and commits:
  - git submodule status
- If submodule URLs were changed or .gitmodules was edited:
  - git submodule sync --recursive
- If a submodule is in a detached HEAD (common), that is normal unless you explicitly want to work on a branch inside the submodule. Checkout a branch inside the submodule when making changes.
- If updates are not appearing, verify the tracked branch:
  - git config -f .gitmodules --get submodule.projects/<name>.branch
  - Then run git submodule update --remote projects/<name>

## Common pitfalls
- Detached HEAD in submodules: Normal for pinned commits; but if you intend to make changes, checkout a branch inside projects/<name> first.
- Uncommitted changes inside submodules: These are not captured by the superproject. Commit or stash inside the submodule before updating or switching.
- Mixing SSH and HTTPS URLs across submodules or between local and CI: Causes auth prompts/failures. Standardize and document your choice.
- Forgetting to commit .gitmodules after add, URL, or branch changes: These changes live in .gitmodules and must be committed.
- Not committing the submodule pointer update in the superproject: After changing a submodule, run git add projects/<name> and commit in the superproject.
- Changing submodule URLs without syncing: Run git submodule sync --recursive to update .git/config.
- CI missing submodules due to not initializing recursively: Ensure git submodule update --init --recursive is used.

## Quick reference / cheat sheet
- Clone with submodules:
  - git clone --recurse-submodules <url>
- Initialize submodules in an existing clone:
  - git submodule init
  - git submodule update
  - or: git submodule update --init --recursive
- Add a new child project under projects/<name> tracking a branch:
  - git submodule add -b <branch> <url> projects/<name>
  - git add .gitmodules projects/<name>
  - git commit -m "Add submodule projects/<name>"
- Update a submodule to latest on tracked branch:
  - git submodule update --remote projects/<name>
  - git add projects/<name>
  - git commit -m "Bump projects/<name>"
- Bulk actions across all submodules:
  - git submodule foreach 'git status'
  - git submodule foreach --recursive 'git pull --ff-only || true'
- Switch the tracked branch:
  - git config -f .gitmodules submodule.projects/<name>.branch <branch>
  - git submodule sync --recursive
  - git add .gitmodules && git commit -m "Track <branch> for projects/<name>"
- Remove a submodule:
  - git submodule deinit -f projects/<name>
  - git rm -f projects/<name>
  - rm -rf .git/modules/projects/<name>
  - git commit -m "Remove submodule projects/<name>"
- Inspect status:
  - git submodule status
- Sync URLs after edits to .gitmodules:
  - git submodule sync --recursive

## Notes on working inside submodules
- Make changes inside projects/<name> as you would in any Git repo: git add, git commit, and optionally git push.
- Return to the superproject root, then stage and commit the submodule pointer update:
  - git add projects/<name>
  - git commit -m "Point projects/<name> to <new_commit>"

By following this guide, you will keep the projects/ folder consistent and ensure submodules integrate smoothly across local development and CI/CD.
