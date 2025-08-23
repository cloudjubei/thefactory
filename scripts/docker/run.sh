#!/bin/bash

set -e

# Get the image name from docker-compose config
IMAGE=$(docker-compose config | grep -A 1 'agent:' | grep image | awk '{print $2}')

# Check if image exists, build if not
if ! docker image inspect "$IMAGE" >/dev/null 2>&1; then
  echo "Image not found. Building..."
  docker-compose build
fi

# Create override file with command as list
OVERRIDE_FILE="docker-compose.override.yml"

echo "version: '3.8'" > "$OVERRIDE_FILE"
echo "services:" >> "$OVERRIDE_FILE"
echo "  agent:" >> "$OVERRIDE_FILE"
echo "    command:" >> "$OVERRIDE_FILE"
for arg in "$@"; do
  printf "      - %s\n" "$arg" >> "$OVERRIDE_FILE"
done

# Trap for graceful shutdown and cleanup
trap 'docker-compose down; rm -f "$OVERRIDE_FILE"' SIGINT SIGTERM EXIT

# Run the container
docker-compose up