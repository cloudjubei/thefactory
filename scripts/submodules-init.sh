#!/usr/bin/env sh

set -e

usage() {
    cat <<EOF
Usage: submodules-init.sh [-h|--help]

Initializes and updates all Git submodules recursively.

This script runs 'git submodule sync --recursive' followed by 'git submodule update --init --recursive'.
It must be run from within a Git repository.

Options:
  -h, --help    Show this help message and exit.

Examples:
  ./scripts/submodules-init.sh
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
    echo "No submodules found to initialize."
    exit 0
fi

echo "Syncing submodule URLs..."
git submodule sync --recursive

echo "Initializing and updating submodules..."
git submodule update --init --recursive

echo "Submodules initialized successfully."
exit 0
