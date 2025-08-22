#!/bin/bash

set -e

# Detect if in git repo and get URL
REPO_URL=$(git config --get remote.origin.url 2>/dev/null || echo "")
REPO_DIR="ai-agent-orchestrator"

if [ -z "$REPO_URL" ]; then
  echo "Not in a git repository. Please provide the repository URL to clone."
  read -p "Enter repo URL: " REPO_URL
  if [ -z "$REPO_URL" ]; then
    echo "No URL provided. Exiting."
    exit 1
  fi
  git clone "$REPO_URL" "$REPO_DIR"
  cd "$REPO_DIR"
else
  echo "Already in repository: $REPO_URL"
fi

# Check for .env file
if [ ! -f ".env" ]; then
  echo ".env file not found."
  if [ -f ".env.example" ]; then
    cp ".env.example" ".env"
    echo "Copied .env.example to .env. Please edit .env and add your API keys."
  else
    echo "Error: .env.example not found. Please create a .env file with necessary API keys. See docs/LOCAL_SETUP.md for details."
    exit 1
  fi
fi

# Build the Docker image
docker build -t ai-agent-orchestrator .

# Output instructions
echo "Docker image built successfully."
echo "To run the container:"
echo "docker run -d --name ai-agent --env-file .env ai-agent-orchestrator"
echo "For more details on periodic running, see docs/RUNNING_IN_DOCKER.md"