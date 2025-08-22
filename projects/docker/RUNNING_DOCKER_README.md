# Running the Agent in Docker

This guide explains how to build and run the autonomous agent inside a Docker container. Running in Docker provides an isolated, consistent environment and allows the agent to run periodically in the background without requiring `cron` or other schedulers on your host machine.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) must be installed and running on your system.
- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) must be installed.

## Step 1: Prepare your `.env` File

The agent requires API keys to function. These are provided via a `.env` file.

1.  Find the root `.env` file in the repository. If it doesn't exist, you can copy `.env.example` to `.env`.
2.  Fill in the required API keys (e.g., `OPENAI_API_KEY`, `GEMINI_API_KEY`, etc.).
3.  Place this `.env` file in a safe and accessible location. The build script will look for it in the directory where it is run, and the `docker run` command needs its path.

**Important:** The `.env` file contains sensitive secrets. Do not commit it to version control.

## Step 2: Build the Docker Image

We provide a convenient script to build the Docker image. This script will clone the latest version of the repository into a temporary directory, build the image, and then clean up.

1.  Navigate to the directory containing your prepared `.env` file.
2.  Run the build script from the root of this repository:

    ```bash
    bash projects/docker/build_docker.sh
    ```

    The script will build a Docker image with the tag `autonomous-agent:latest`.

Alternatively, if you wish to build manually from your local clone of the repository, you can run this command from the project root:

```bash
docker build -f projects/docker/Dockerfile -t autonomous-agent:latest .
```

## Step 3: Run the Agent Container

Once the image is built, you can run the agent in a container. The `build_docker.sh` script will print this command for you, customized with the path to your `.env` file.

A typical `docker run` command looks like this:

```bash
docker run -d --restart always --env-file /path/to/your/.env --name my-agent autonomous-agent:latest
```

### Command Breakdown:

-   `docker run`: The command to start a new container.
-   `-d`: Detached mode. Runs the container in the background.
-   `--restart always`: Ensures the container restarts automatically if it stops for any reason (e.g., after a system reboot).
-   `--env-file /path/to/your/.env`: **Crucial.** This securely provides your API keys and other environment variables from your `.env` file to the container. **Replace `/path/to/your/.env` with the actual, absolute path to your file.**
-   `--name my-agent`: A convenient name for your container, making it easy to manage.
-   `autonomous-agent:latest`: The name and tag of the image to use.

## How it Works: Periodic Execution

The Docker container uses an entrypoint script that runs the agent in an infinite loop. After each run, it waits for a specified interval (defaulting to 1 hour) before starting the next run.

-   **No Host Scheduler Needed:** You do not need to set up `cron` or any other task scheduler on your host machine. The container manages its own periodic execution.
-   **Isolation:** The agent and its dependencies are completely contained within the Docker environment, preventing any conflicts with your host system's software.

## Customizing the Agent's Behavior

You can customize the agent's execution by passing environment variables (`-e`) to the `docker run` command.

-   `AGENT_PERSONA`: Sets the agent persona to run. (Default: `developer`)
-   `SLEEP_INTERVAL`: The time in seconds to wait between agent runs. (Default: `3600`)
-   `TASK_ID`: An optional task ID to focus on a specific task.

### Example with Customizations:

This command runs the `planner` agent, targeting task `42`, with a 5-minute interval between runs.

```bash
docker run -d --restart always \
  --env-file /path/to/your/.env \
  -e AGENT_PERSONA=planner \
  -e SLEEP_INTERVAL=300 \
  -e TASK_ID=42 \
  --name my-planner-agent \
  autonomous-agent:latest
```

## Managing the Container

-   **View logs:** `docker logs my-agent` (use `-f` to follow the log stream)
-   **Stop the container:** `docker stop my-agent`
-   **Start the container:** `docker start my-agent`
-   **Remove the container:** `docker rm my-agent` (must be stopped first)
