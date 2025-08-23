# Docker Setup Guide

This guide explains how to run the agent inside Docker with a single command, reusing your existing .env configuration.

## Prerequisites
- Docker (Engine/Desktop)
  - Install: https://docs.docker.com/get-docker/
- Docker Compose
  - Compose v2 (docker compose) is included with modern Docker installs.
  - Compose v1 (docker-compose) is also supported. The script auto-detects either.

Verify installation:
- docker --version
- docker compose version or docker-compose --version

## One-command quick start
1) Ensure your environment variables are set in a .env file at the repository root.
   - The Docker setup reuses the existing .env and mounts it into the container read-only.
   - If you dont have one, create it (for example by copying any example file) and add your provider/API keys as needed.

2) From the repo root, run the Docker launcher script and pass your agent arguments:
- scripts/docker/run.sh --agent developer --task 2

The script will:
- Load your .env into the environment and mount it into the container at /app/.env (read-only).
- Create a default scripts/docker/Dockerfile and scripts/docker/docker-compose.yml if missing.
- Build the Docker image on first run (or if not present).
- Start the container with docker compose and run python run.py with your arguments.
- Clean up containers on exit (Ctrl-C) via a trap.

## Passing arguments to the agent
Pass arguments to scripts/docker/run.sh exactly as you would to run.py. The script forwards everything to the agent inside the container via AGENT_ARGS.

Examples:
- Developer agent on task 2:
  - scripts/docker/run.sh --agent developer --task 2
- Planner agent on task 5 in single mode with a specific model:
  - scripts/docker/run.sh --agent planner --task 5 --mode single --model gpt-4o
- Developer agent targeting a specific feature (e.g., 4.5):
  - scripts/docker/run.sh --agent developer --task 4 --feature 4.5

Inside the container, the command effectively becomes:
- python run.py <your-arguments>

## Environment handling (.env reuse)
- The script auto-loads the repositorys .env (if present) into its environment and also bind-mounts it into the container at /app/.env as read-only.
- This means your existing configuration (API keys, Git identity, etc.) is reused without extra steps.
- If you prefer not to mount the file, remove or rename .env before running the script and set environment variables via another mechanism.

## Logs, stopping, and rebuilds
- Logs stream in your terminal. Press Ctrl-C to stop; the script performs a graceful cleanup (docker compose down).
- To force a rebuild, you can remove the image or run: docker compose -f scripts/docker/docker-compose.yml build --no-cache
- You can set a custom image name by exporting IMAGE_NAME before running the script.

## Troubleshooting
- If the script reports that Docker Compose is missing, install Docker Desktop/Engine and ensure either docker compose or docker-compose is on your PATH.
- Ensure Docker is running.
- Verify your .env values are correct and available to the container (a copy is mounted at /app/.env).

## Notes
- The Docker setup is designed for minimal user configuration: a single command can build and run the agent.
- scripts/docker/run.sh is an executable Bash script and should run directly from Unix-like shells. On Windows, run it inside WSL or Git Bash.
