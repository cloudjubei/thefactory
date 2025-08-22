#!/bin/bash
set -e # Exit immediately if a command exits with a non-zero status.

# --- Configuration ---
# The Git repository URL for the project.
GIT_REPO_URL="https://github.com/cloudjubei/thefactory.git"
# The name and tag for the Docker image.
IMAGE_NAME="autonomous-agent"
IMAGE_TAG="latest"

# --- Script Logic ---
echo "--- Autonomous Agent Docker Build Script ---"

# 1. Check for dependencies: git and docker
if ! command -v git &> /dev/null; then
    echo "Error: git is not installed. Please install git and try again."
    exit 1
fi
if ! command -v docker &> /dev/null; then
    echo "Error: docker is not installed. Please install Docker and try again."
    exit 1
fi

# 2. Check for the .env file in the current directory
# The script expects to be run from a directory containing the .env file.
ENV_FILE_PATH="$(pwd)/.env"
if [ ! -f "$ENV_FILE_PATH" ]; then
    echo "Error: .env file not found in the current directory ($(pwd))."
    echo "Please create a .env file with your API keys before running this script."
    exit 1
fi
echo "Found .env file at $ENV_FILE_PATH"

# 3. Clone the repository into a temporary directory
BUILD_DIR=$(mktemp -d)
echo "Cloning repository $GIT_REPO_URL into temporary directory: $BUILD_DIR"
git clone "$GIT_REPO_URL" "$BUILD_DIR"

# 4. Copy the .env file into the cloned repository for the 'docker run' step later
cp "$ENV_FILE_PATH" "$BUILD_DIR/.env"
echo ".env file copied to $BUILD_DIR/.env for reference, but will not be in image."

# 5. Build the Docker image
echo "Building Docker image '$IMAGE_NAME:$IMAGE_TAG'..."
# We run docker build from within the cloned repository directory to set the build context.
(cd "$BUILD_DIR" && docker build -f projects/docker/Dockerfile -t "$IMAGE_NAME:$IMAGE_TAG" .)
echo "Docker image built successfully."

# 6. Clean up the temporary build directory
echo "Cleaning up temporary build directory..."
rm -rf "$BUILD_DIR"
echo "Cleanup complete."

# 7. Provide instructions for running the container
echo ""
echo "--- Build Complete! ---"
echo "To run the agent, use the following command:"
echo ""
echo "docker run -d --restart always --env-file \"$ENV_FILE_PATH\" --name my-agent $IMAGE_NAME:$IMAGE_TAG"
echo ""
echo "Explanation of the command:"
echo "  -d                  : Run the container in detached mode (in the background)."
echo "  --restart always    : Automatically restart the container if it stops."
echo "  --env-file \"$ENV_FILE_PATH\" : Provides your API keys from the .env file."
echo "  --name my-agent     : A friendly name for your container."
echo "  $IMAGE_NAME:$IMAGE_TAG : The image you just built."
echo ""
echo "You can customize the agent's behavior with environment variables:"
echo "  -e AGENT_PERSONA=developer  # The agent to run (default: developer)"
echo "  -e SLEEP_INTERVAL=3600      # Time in seconds between runs (default: 3600)"
echo "  -e TASK_ID=5                # Optional: target a specific task ID"
echo ""
echo "Example with custom options:"
echo "docker run -d --restart always --env-file \"$ENV_FILE_PATH\" -e AGENT_PERSONA=planner -e TASK_ID=10 --name my-planner-agent $IMAGE_NAME:$IMAGE_TAG"
echo ""
