#!/bin/bash

set -e

# Change to the directory of the script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Get the image name from docker-compose
IMAGE=$(docker-compose config --images | head -1)

# Check if the image is already built
if ! docker image inspect "$IMAGE" >/dev/null 2>&1; then
  echo "Building Docker image..."
  docker-compose build
fi

# Create temporary override file to pass arguments as command
OVERRIDE_FILE="docker-compose.override.yml"

cat > "$OVERRIDE_FILE" <<EOF
services:
  agent:
    command:
EOF

for arg in "$@"; do
  esc_arg="${arg//\"/\\\"}"
  echo "      - \"$esc_arg\"" >> "$OVERRIDE_FILE"
done

# Trap signals for graceful shutdown
trap 'docker-compose down; rm -f "$OVERRIDE_FILE"' SIGINT SIGTERM

# Start the container in detached mode
echo "Starting the agent container..."
docker-compose up -d

# Get the container ID
CONTAINER_ID=$(docker-compose ps -q agent)

if [ -z "$CONTAINER_ID" ]; then
  echo "Failed to get container ID."
  docker-compose down
  rm -f "$OVERRIDE_FILE"
  exit 1
fi

# Wait for the container to finish
docker wait "$CONTAINER_ID"

# Cleanup after completion
docker-compose down
rm -f "$OVERRIDE_FILE"

echo "Agent run completed."