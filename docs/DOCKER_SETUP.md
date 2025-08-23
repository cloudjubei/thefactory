# Docker Setup Guide

This document provides instructions for setting up and running the AI agent in a Docker container. The setup is designed to be minimal, reusing existing configurations like the `.env` file, and allows launching the agent with a single script.

## Prerequisites

To run the agent in Docker, ensure you have the following installed:

- **Docker**: Required for building and running containers. Download from [Docker's official website](https://www.docker.com/products/docker-desktop).
- **Docker Compose**: Used for defining and running multi-container Docker applications. It is included with Docker Desktop, or install separately from [Docker Compose documentation](https://docs.docker.com/compose/install/).

## Setup

All Docker-related files are located in `scripts/docker/`. This includes:
- `Dockerfile`: Defines the Docker image based on Python 3.11, copies the project files, installs dependencies from `requirements.txt`, and sets the entrypoint to `run.py`.
- `docker-compose.yml`: Configures the service, builds the image from the project root, and mounts necessary volumes:
  - `.env` (read-only) for environment variables.
  - `projects/` and `tasks/` directories for project data.
- `run.sh`: A bash script to build (if needed), start the container with provided arguments, wait for completion, and clean up.

No additional configuration is needed beyond having a valid `.env` file in the project root, as it is automatically mounted into the container.

## Running the Agent in Docker

Use the `scripts/docker/run.sh` script to launch the agent. This script:
1. Builds the Docker image if it doesn't exist.
2. Creates a temporary `docker-compose.override.yml` to pass your arguments as the container's command.
3. Starts the container in detached mode using `docker-compose up -d`.
4. Waits for the container to finish execution.
5. Cleans up by shutting down the container and removing the override file.

### Usage

Navigate to the `scripts/docker/` directory or run the script from the project root. Pass the same arguments as you would to `run.py` (e.g., `--agent`, `--task`, etc.).

```bash
# Example: Run the developer agent on task 4 using the default model
./scripts/docker/run.sh --agent developer --task 4
```

Or with more options:

```bash
./scripts/docker/run.sh --agent developer --model gpt-4-turbo --task 4 --feature 4.5 --mode single
```

### Interacting with the Agent

- The script runs the agent to completion in the background (detached mode).
- To view real-time logs during execution, open a new terminal and run:
  ```bash
  docker-compose -f scripts/docker/docker-compose.yml logs -f agent
  ```
- The container automatically stops after the agent finishes, and the script cleans up. Any output or changes (e.g., commits) will be handled as per the agent's logic, with mounted volumes ensuring data persistence.

### Notes
- The setup reuses the project's `.env` file, so ensure it is configured with necessary API keys and Git details.
- If the image needs rebuilding (e.g., after changes to `requirements.txt`), the script will handle it automatically.
- For troubleshooting, check Docker logs or ensure volumes are correctly mounted.

This setup minimizes steps: clone the repo, configure `.env`, and run the script with arguments.