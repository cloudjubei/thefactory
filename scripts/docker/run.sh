#!/usr/bin/env bash
set -euo pipefail

# Resolve directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
COMPOSE_FILE="$REPO_ROOT/scripts/docker/docker-compose.yml"
DOCKERFILE="$REPO_ROOT/scripts/docker/Dockerfile"

cd "$REPO_ROOT"

# Load environment variables from .env if present
if [[ -f "$REPO_ROOT/.env" ]]; then
  set -a
  # shellcheck disable=SC1090
  . "$REPO_ROOT/.env"
  set +a
fi

# Determine image name from env or repo name
IMAGE_NAME_DEFAULT="$(basename "$REPO_ROOT" | tr '[:upper:]' '[:lower:]')-agent"
export IMAGE_NAME="${IMAGE_NAME:-$IMAGE_NAME_DEFAULT}"

# Forward all script args to the agent process
export AGENT_ARGS="$*"

# Ensure docker dir exists
mkdir -p "$REPO_ROOT/scripts/docker"

# Create a default Dockerfile if missing to enable single-command usage
if [[ ! -f "$DOCKERFILE" ]]; then
  cat > "$DOCKERFILE" <<'EOF'
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends git curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application source
COPY . /app

# Default run; args can be overridden via AGENT_ARGS
CMD ["bash", "-lc", "python run.py ${AGENT_ARGS:-'--agent developer'}"]
EOF
fi

# Create a default docker-compose.yml if missing
if [[ ! -f "$COMPOSE_FILE" ]]; then
  cat > "$COMPOSE_FILE" <<'EOF'
version: "3.9"
services:
  agent:
    image: ${IMAGE_NAME:-agent-image}
    build:
      context: .
      dockerfile: scripts/docker/Dockerfile
    working_dir: /app
    environment:
      - AGENT_ARGS
    volumes:
      - ./:/app
      - ./.env:/app/.env:ro
    tty: true
    # Use bash -lc so we can expand AGENT_ARGS correctly
    command: >
      bash -lc "python run.py ${AGENT_ARGS:-'--agent developer'}"
EOF
fi

# Choose docker compose command (v1 or v2)
if command -v docker-compose >/dev/null 2>&1; then
  COMPOSE_CMD=(docker-compose)
elif docker compose version >/dev/null 2>&1; then
  COMPOSE_CMD=(docker compose)
else
  echo "Error: docker-compose or 'docker compose' is required." >&2
  exit 1
fi

# Build the image if not present
if ! docker image inspect "$IMAGE_NAME:latest" >/dev/null 2>&1; then
  echo "Docker image '$IMAGE_NAME:latest' not found. Building..."
  docker build -t "$IMAGE_NAME:latest" -f "$DOCKERFILE" "$REPO_ROOT"
else
  echo "Docker image '$IMAGE_NAME:latest' already exists."
fi

cleanup() {
  echo "\nGracefully shutting down containers..."
  "${COMPOSE_CMD[@]}" -f "$COMPOSE_FILE" down --remove-orphans || true
}
trap cleanup INT TERM EXIT

echo "Starting agent via docker-compose. Arguments: $AGENT_ARGS"
"${COMPOSE_CMD[@]}" -f "$COMPOSE_FILE" up --build --remove-orphans --abort-on-container-exit
