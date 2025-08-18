# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install git and gh CLI. gh CLI is needed for 'submit_for_review'.
# git is needed for basic git operations by the agent itself.
RUN apt-get update && \
    apt-get install -y --no-install-recommends git curl && \
    curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg && \
    chmod go+rw /usr/share/keyrings/githubcli-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null && \
    apt-get update && \
    apt-get install -y --no-install-recommends gh && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the current directory into the container at /app
# This should be the project root when building
COPY . .

# Ensure scripts are executable (optional, but good practice if not done in git)
# RUN chmod +x scripts/*.py

# Set environment variables if needed (e.g., for non-production API keys)
# ENV OPENAI_API_KEY=your_key

# Command to run the agent. This can be overridden by 'docker run'
CMD ["python3", "scripts/run_local_agent.py", "--task", "11"]
