# Running the Project in a Container

## 1. Purpose
This document outlines the steps to run the autonomous AI agent project within an isolated container environment. Running the project in a container ensures reproducibility, consistency across different environments, and prevents the agent from making unintended changes to the host machine. This is particularly useful for automated testing, continuous integration, and deploying agents in controlled environments.

## 2. Prerequisites
- **Docker:** Ensure Docker is installed and running on your system.
  - [Install Docker Engine](https://docs.docker.com/engine/install/)

## 3. Workflow Steps

### 3.1. Prepare Dockerfile
While this document doesn't provide a complete `Dockerfile` for the entire project due to its evolving nature, a basic `Dockerfile` might look like this for a Python-based agent:

```dockerfile
# Start with a base Python image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Command to run the agent (example, adjust as needed)
# CMD ["python", "scripts/run_local_agent.py", "--mode", "single", "--task", "1"]
```
You would place this `Dockerfile` in the root of your project.

### 3.2. Build the Docker Image
Navigate to the root directory of your project (where the `Dockerfile` is located) and run:

```bash
docker build -t autonomous-agent .
```
This command builds a Docker image named `autonomous-agent` from your `Dockerfile`.

### 3.3. Run the Container
You can run the container and mount your local project directory into it, allowing the agent inside the container to access and modify your files.

```bash
docker run -it --rm \
  -v "$(pwd):/app" \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \ # Pass API key if using cloud LLMs
  autonomous-agent \
  python scripts/run_local_agent.py --mode single --task 11
```

**Explanation of the command:**
-   `docker run`: Command to run a new container.
-   `-it`: Allocates a pseudo-TTY and keeps stdin open, allowing for interactive processes.
-   `--rm`: Automatically remove the container when it exits.
-   `-v "$(pwd):/app"`: Mounts your current host directory (`$(pwd)`) to the `/app` directory inside the container. This is crucial for the agent to read and write files in your project.
-   `-e OPENAI_API_KEY=$OPENAI_API_KEY`: Passes environment variables (like API keys for LLMs) from your host to the container. Adjust as needed for your chosen LLM.
-   `autonomous-agent`: The name of the Docker image to use.
-   `python scripts/run_local_agent.py --mode single --task 11`: The command executed inside the container, running the agent for a specific task.

## 4. Considerations
-   **Isolation:** The container provides a clean, isolated environment for each run, ensuring that dependencies and system configurations don't interfere with the agent's operation.
-   **Reproducibility:** Anyone with Docker can replicate the exact environment, making development and testing consistent across teams and machines.
-   **Resource Management:** Docker allows for resource limiting (CPU, memory), which can be useful when running agents in production or on shared infrastructure.
-   **Security:** By default, containers offer a degree of isolation from the host system, which can prevent unintended side effects on your local machine. However, mounting volumes (as shown above) means the container can modify the host's files in the mounted directory. For stricter isolation, consider running without volume mounts and transferring files in/out, or using more advanced container orchestration tools with dedicated storage.
