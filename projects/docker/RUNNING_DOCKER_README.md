# Running the AI Agent Orchestrator in Docker

This guide provides step-by-step instructions for building and running the project in Docker.

## Prerequisites

- Docker installed on your system.
- Git installed for cloning the repository.

## Step 1: Clone the Repository

```bash
git clone <your_repository_url>
cd <repository_directory>
```

## Step 2: Prepare the .env File

The agent requires API keys for LLM services.

1. Copy the example file:

```bash
cp .env.example .env
```

2. Open `.env` in a text editor and add your API keys. For example:

```
OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

Refer to `docs/LOCAL_SETUP.md` for more details on local configuration, which applies similarly here.

## Step 3: Build the Docker Image

Use the provided build script to build the Docker image.

```bash
./scripts/build_docker.sh
```

This script will handle building the image (assuming it runs `docker build -t ai-agent-orchestrator .` or similar).

## Step 4: Run the Docker Container

To run the container:

```bash
docker run -d --name ai-agent --env-file .env ai-agent-orchestrator
```

This runs the agent using the prepared `.env` file.

## Step 5: Running the Container Periodically

To run the container on a periodic basis (e.g., every hour), you can set up a cron job on the host machine.

1. Create a script to restart the container, e.g., `run_agent_periodic.sh`:

```bash
#!/bin/bash
docker stop ai-agent || true
docker rm ai-agent || true
docker run -d --name ai-agent --env-file .env ai-agent-orchestrator
```

2. Make it executable:

```bash
chmod +x run_agent_periodic.sh
```

3. Add to crontab (runs every hour):

```bash
crontab -e
```

Add the line:

```
0 * * * * /path/to/run_agent_periodic.sh
```

This ensures the container is restarted periodically, allowing the agent to run tasks at intervals.