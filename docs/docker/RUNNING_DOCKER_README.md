# Running the Agent in Docker

This guide details how to build and run the autonomous AI agent within a Docker container. This provides an isolated environment for execution, preventing conflicts with your host system and ensuring consistent behavior.

## Prerequisites

-   **Docker Desktop:** Install Docker Desktop for your operating system from [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop).

## I. Building the Docker Image

1.  **Navigate to the project root:**
    ```bash
    cd /path/to/your/agent-repo
    ```

2.  **Place your Dockerfile:**
    Ensure the `Dockerfile` provided in `docs/docker/Dockerfile` is in the `docs/docker/` directory. You might want to copy it to the project root for building or adjust the build context. For simplicity, we assume you'll build from the project root and reference the `docs/docker/Dockerfile`.

3.  **Build the image:**
    From the **project root**, run the following command. This will build an image named `agent-project`.
    ```bash
    docker build -t agent-project -f docs/docker/Dockerfile .
    ```
    The `-f docs/docker/Dockerfile` flag tells Docker to use the Dockerfile located in the `docs/docker/` directory, while `.` indicates the build context is the current directory (project root), allowing access to `requirements.txt` and other project files.

## II. Preparing Environment Variables (API Keys)

The agent requires API keys for cloud LLMs (e.g., OpenAI, Groq, Gemini) or configuration for local LLMs (Ollama). These are typically loaded from a `.env` file.

1.  **Create your `.env` file:**
    In the **project root**, copy the example file:
    ```bash
    cp .env.example .env
    ```

2.  **Edit `.env`:**
    Open the new `.env` file and add your necessary API keys or adjust Ollama settings. **This file will be mounted into the container at runtime.**

## III. Running the Agent Container

You can run the agent in single-task mode or continuous mode.

1.  **Mount the current repository:**
    You need to mount your local project directory into the Docker container. This allows the agent inside the container to see and modify your local files, including `TASKS.md` and other documentation.

2.  **Run with an LLM (e.g., OpenAI's GPT-4o):**
    This command mounts your current directory (`$(pwd)`) to `/app` inside the container and passes the `.env` file as environment variables.
    ```bash
    docker run --rm \
      -v "$(pwd)":/app \
      --env-file .env \
      agent-project \
      python3 scripts/run_local_agent.py --model gpt-4o --task 11 --mode single
    ```
    -   `--rm`: Automatically remove the container when it exits.
    -   `-v "$(pwd)":/app`: Mounts your current host directory to `/app` in the container.
    -   `--env-file .env`: Loads environment variables from your local `.env` file into the container.
    -   `agent-project`: The name of the Docker image we built.
    -   `python3 scripts/run_local_agent.py ...`: The command to execute inside the container.

3.  **Running with a local Ollama instance (on host):**
    If you have Ollama running directly on your host machine and want the Dockerized agent to use it, you'll need to configure Docker to allow the container to access your host's network.

    ```bash
    docker run --rm \
      -v "$(pwd)":/app \
      --env-file .env \
      --network host \
      agent-project \
      python3 scripts/run_local_agent.py --model ollama/llama3 --task 11 --mode single
    ```
    -   `--network host`: Allows the container to share the host's network namespace, enabling access to services running on `localhost` (like Ollama).
        **Note:** Using `--network host` has security implications as it gives the container full access to your host's network interfaces. Use with caution.

## IV. Further Considerations

-   **API Key Management:** For production deployments, consider more secure methods for managing API keys (e.g., Docker secrets, cloud key management services) instead of directly mounting `.env`.
-   **Persistent Data:** If the agent needs to store persistent data (e.g., logs, databases) that should survive container restarts, you will need to define additional Docker volumes.
-   **GitHub Authentication:** The `gh auth login` step described in `docs/LOCAL_SETUP.md` is critical. When running in Docker, you'll need to ensure the agent has access to your GitHub credentials. This often involves mounting your `.ssh` directory or a token. A simpler approach for the agent to push is to use a GitHub PAT with `repo, workflow` scopes directly as an environment variable or via `gh auth login` from within the running container (which is typically done in CI/CD, not local Docker). For this basic setup, relying on local `gh auth login` is assumed, which means the host's git setup manages the pushing.
