# Docker Setup Guide

This guide explains how to set up and run the project in a Docker container, allowing you to launch the agent with minimal configuration. It adheres to the guidelines in `docs/PROJECTS_GUIDE.md` for project management.

## Prerequisites

- **Docker**: Ensure Docker is installed on your machine. Download from [docker.com](https://www.docker.com/products/docker-desktop).

- **Docker Compose**: Required for managing multi-container Docker applications. It is included with Docker Desktop for Windows and Mac, or can be installed separately on Linux from [docs.docker.com/compose/install](https://docs.docker.com/compose/install/).

## Instructions

1. **Clone the Repository**

   If you haven't already, clone the repository to your local machine:

   ```
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Configure Environment Variables**

   The Docker setup reuses the existing `.env` file in the repository root. Ensure it is configured as per `docs/LOCAL_SETUP.md`. This includes API keys, Git configuration, and any other necessary variables. Data from the current project, especially the `.env` file, is reused to minimize configuration.

3. **Run the Docker Script**

   Use the `scripts/docker/run.sh` script to start and interact with the agent in a Docker container. The script handles building the image if necessary, creates a temporary override file, and passes any arguments you provide to the agent's command inside the container. This allows running the project and launching an agent with a single command.

   ### Usage

   From the repository root:

   ```
   ./scripts/docker/run.sh [arguments]
   ```

   The arguments are the same as those used for local runs (see `docs/LOCAL_SETUP.md`), such as `--agent`, `--model`, `--task`, `--feature`, `--mode`.

   ### Example

   To run the developer agent on task 4 using the model gpt-4-turbo:

   ```
   ./scripts/docker/run.sh --agent developer --model gpt-4-turbo --task 4
   ```

   This will:
   - Check if the Docker image exists; build it using `docker-compose build` if not.
   - Create a `docker-compose.override.yml` with the provided arguments as the command.
   - Start the container using `docker-compose up`.
   - The agent will run inside the container with the specified parameters.

4. **Interacting with the Agent**

   Once running, the agent's output will be displayed in the terminal. You can interact as needed if the mode allows (e.g., continuous mode). To stop, press Ctrl+C. The script traps signals for graceful shutdown, running `docker-compose down` and removing the override file.

5. **Notes**

   - The setup mounts necessary volumes (e.g., for `.env` and project files) to reuse existing data and configurations.
   - For projects managed as submodules under `projects/`, follow `docs/PROJECTS_GUIDE.md`.
   - If issues arise, verify Docker is running, check logs with `docker-compose logs`, or ensure the `.env` is correctly set up.