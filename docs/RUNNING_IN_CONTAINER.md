# Running in a Container

This document outlines the steps to run the project's agent within a Docker container. This approach provides an isolated, consistent, and reproducible environment, ensuring that the agent's operations do not affect your host machine and that dependencies are self-contained.

## Purpose

The primary purpose of running the agent in a container is to:
-   **Isolation**: Prevent the agent's dependencies and operations from interfering with your host system.
-   **Consistency**: Ensure the agent runs in an identical environment every time, regardless of the host machine's configuration.
-   **Reproducibility**: Make it easy for anyone to set up and run the agent with the same environment.

## Prerequisites

-   **Docker**: Ensure Docker is installed and running on your system. You can download it from [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop).

## Steps to Run the Agent in a Container

### 1. Create a `Dockerfile`

In the root of your project directory, create a file named `Dockerfile` with the following content:

```dockerfile
# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
# Consider adding a .dockerignore file to exclude unnecessary files like .git, __pycache__, etc.
COPY . /app

# Install any needed packages specified in requirements.txt
# Assuming requirements.txt is at the root of the copied context.
RUN pip install --no-cache-dir -r requirements.txt

# The ENTRYPOINT defines the default command to execute when the container starts.
# Users can override this by providing arguments to 'docker run'.
# Example: docker run agent-project --task 1 --mode single --model ollama/llama3
ENTRYPOINT ["python3", "scripts/run_local_agent.py"]
```

### 2. Build the Docker Image

Navigate to your project's root directory in your terminal and run the following command to build the Docker image. This command builds an image named `agent-project` based on your `Dockerfile`.

```bash
docker build -t agent-project .
```

This process might take a few minutes as Docker downloads the base image and installs dependencies.

### 3. Run the Docker Container

Once the image is built, you can run the agent inside a container. Arguments for `scripts/run_local_agent.py` are passed after the image name.

#### Basic Run (e.g., to run task 1 in single mode):

```bash
docker run --rm -it agent-project --task 1 --mode single
```

**Explanation of `docker run` flags:**
-   `--rm`: Automatically remove the container when it exits.
-   `-it`: Allocate a pseudo-TTY and keep stdin open, allowing for interactive processes (useful for debugging).
-   `agent-project`: The name of the Docker image you just built.
-   `--task 1 --mode single`: These are the arguments passed directly to `scripts/run_local_agent.py` inside the container.

#### Running with Cloud LLMs (via Environment Variables):

If you are using cloud LLMs (like OpenAI, Groq, Gemini) that require API keys, you must pass these as environment variables to the Docker container:

```bash
docker run --rm -it \
  -e OPENAI_API_KEY="your_openai_api_key" \
  -e GROQ_API_KEY="your_groq_api_key" \
  # Add other API keys as needed
  agent-project \
  --task 1 --mode single --model gpt-4o
```

Replace `"your_openai_api_key"` and `"your_groq_api_key"` with your actual API keys.

#### Running with Ollama (if Ollama is on the host machine):

If your Ollama instance is running directly on your host machine and you want the container to connect to it, you can make the host network accessible to the container by setting the `LITELLM_OLLAMA_BASE_URL` environment variable and ensuring Docker can route to the host.

For Docker Desktop users, `host.docker.internal` often resolves to the host machine's IP address:

```bash
docker run --rm -it \
  -e LITELLM_OLLAMA_BASE_URL="http://host.docker.internal:11434" \
  agent-project \
  --task 1 --mode single --model ollama/llama3
```

For Linux users, or if `host.docker.internal` doesn't work, you might need to use `--network=host` (less isolated) or explicitly get your host's IP and pass it.

```bash
# Less isolated, but can simplify host access on Linux
docker run --rm -it --network=host \
  agent-project \
  --task 1 --mode single --model ollama/llama3
```
(Note: Using `--network=host` makes the container share the host's network namespace, which reduces isolation. It's generally preferred to use `host.docker.internal` or link dedicated Ollama containers.)

By following these steps, you can reliably run the autonomous agent in an isolated containerized environment.
