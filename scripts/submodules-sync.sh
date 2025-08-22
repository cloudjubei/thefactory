#!/usr/bin/env sh

set -e

usage() {
    cat <<EOF
Usage: submodules-sync.sh [-h|--help]

Synchronizes submodule URLs.

This script runs 'git submodule sync --recursive' to update submodule URLs
from .gitmodules into the local repository configuration.
It must be run from within a Git repository.

Options:
  -h, --help    Show this help message and exit.

Examples:
  ./scripts/submodules-sync.sh
EOF
}

# Main script execution

if [ "$#" -gt 0 ]; then
    case "$1" in
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "Error: Unknown option '$1'"
            usage
            exit 1
            ;;
    esac
fi

# Check if inside a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "Error: Not a git repository. Please run this script from the root of a git repository." >&2
    exit 1
fi

# Check if .gitmodules exists and is not empty
if [ ! -s .gitmodules ]; then
    echo "No submodules found to sync."
    exit 0
fi

echo "Syncing submodule URLs..."
git submodule sync --recursive

echo "Submodule URLs synced successfully."
exit 0
