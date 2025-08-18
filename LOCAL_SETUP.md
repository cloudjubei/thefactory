# Local Agent Setup and Usage Guide (macOS)

This guide provides step-by-step instructions to set up and run the autonomous AI agent on your local machine.

## Step 1: Core Tool Setup

1.  **Install Prerequisites via Homebrew:**
    Open `Terminal` and run the following. This installs Git, Python, the GitHub CLI, and Ollama.
    ```bash
    # Install Homebrew if you don't have it
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Install tools
    brew install git python gh ollama
    ```

2.  **Authenticate with GitHub:**
    This allows the agent to create pull requests for you.
    ```bash
    gh auth login
    ```
    Follow the prompts, selecting `HTTPS` as your preferred protocol.

## Step 2: Project and Dependency Setup

1.  **Install Python Libraries:**
    Navigate to the project's root directory in your terminal and run:
    ```bash
    pip3 install -r requirements.txt
    ```

2.  **Configure API Keys (for Cloud Models):**
    If you only plan to use local models via Ollama, you can skip this step.
    ```bash
    # Copy the example .env file
    cp .env.example .env
    ```
    Now, open the new `.env` file in a text editor. Get your Gemini API key from [aistudio.google.com](https://aistudio.google.com) and paste it into the file.

## Step 3: Running the Agent

### For Local Models (Ollama)

1.  **Start the Ollama Service:**
    Ollama needs to be running in the background. The `brew` command handles this for you.
    ```bash
    brew services start ollama
    ```
    *(You only need to do this once. It will now start automatically when you log in.)*

2.  **Download a Model:**
    If you haven't already, pull the Llama 3 model (one-time ~4.7GB download).
    ```bash
    ollama pull llama3
    ```

3.  **Run the Agent:**
    ```bash
    # Execute one task with the local Llama 3 model
    python3 scripts/run_local_agent.py --model ollama/llama3
    ```    *(Since this is the default, `python3 scripts/run_local_agent.py` also works)*


### For Cloud Models (Gemini)

1.  **Ensure your `.env` file is set up** (from Step 2.2).

2.  **Run the Agent:**
    ```bash
    # Execute one task with Gemini 1.5 Flash
    python3 scripts/run_local_agent.py --model gemini/gemini-1.5-flash
    ```

### Execution Modes

-   **Run in Continuous Mode:** To make the agent complete all available tasks instead of just one, add the `--mode continuous` flag to any of the commands above.
    ```bash
    # Example: Run continuously with the local model
    python3 scripts/run_local_agent.py --mode continuous
    ``````
---
**EXECUTION COMPLETE.**

All specified tasks are now complete. The project has been significantly refactored based on your feedback. The agent is now more robust, easier to extend, and correctly documented. The stopping point has been reached. You can now follow the new, accurate instructions in `LOCAL_SETUP.md`.