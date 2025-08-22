#!/usr/bin/env sh

set -e

usage() {
    cat <<EOF
Usage: project-add.sh <repo_url> <name> [--branch BRANCH]

Adds a new child project as a Git submodule under the 'projects/' directory.

Arguments:
  <repo_url>    The URL of the repository to add.
  <name>        A short name for the project. This will be the directory name under projects/.
                Must not contain path separators.

Options:
  --branch BRANCH  The branch to track. If not specified, the remote's default branch is used.
  -h, --help       Show this help message and exit.

Examples:
  ./scripts/project-add.sh git@github.com:user/my-project.git my-project
  ./scripts/project-add.sh https://github.com/user/another.git another-proj --branch develop
EOF
}

# Argument parsing
REPO_URL=""
NAME=""
BRANCH_ARG=""

while [ "$#" -gt 0 ]; do
    case "$1" in
        -h|--help)
            usage
            exit 0
            ;;
        --branch)
            if [ -z "$2" ]; then
                echo "Error: --branch requires an argument." >&2
                exit 1
            fi
            BRANCH_ARG="-b $2"
            shift
            shift
            ;;
        -*)
            echo "Error: Unknown option '$1'" >&2
            usage
            exit 1
            ;;
        *)
            if [ -z "$REPO_URL" ]; then
                REPO_URL="$1"
            elif [ -z "$NAME" ]; then
                NAME="$1"
            else
                echo "Error: Too many arguments." >&2
                usage
                exit 1
            fi
            shift
            ;;
    esac
done

if [ -z "$REPO_URL" ] || [ -z "$NAME" ]; then
    echo "Error: Missing required arguments <repo_url> and <name>." >&2
    usage
    exit 1
fi

# --- Start main execution ---

# Check if inside a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "Error: Not a git repository. Please run this script from the root of a git repository." >&2
    exit 1
fi

# Validate project name
case "$NAME" in
    */*|*..*)
        echo "Error: Project name '$NAME' cannot contain path separators ('/') or traversal components ('..')." >&2
        exit 1
        ;;
    *)
        ;;
esac

PROJECTS_DIR="projects"
TARGET_PATH="$PROJECTS_DIR/$NAME"

# Ensure projects/ directory exists
if [ ! -d "$PROJECTS_DIR" ]; then
    echo "Creating directory: $PROJECTS_DIR"
    mkdir -p "$PROJECTS_DIR"
fi

# Check if target path already exists
if [ -e "$TARGET_PATH" ]; then
    echo "Error: Target path '$TARGET_PATH' already exists." >&2
    exit 1
fi

# Add the submodule
echo "Adding submodule '$NAME' from '$REPO_URL' to '$TARGET_PATH'..."

# We use sh -c to correctly handle the optional branch argument string
# shellcheck disable=SC2086
sh -c "git submodule add $BRANCH_ARG -- '$REPO_URL' '$TARGET_PATH'"

echo "Successfully added project '$NAME' as a submodule."
exit 0
