# Local Agent Setup and Usage Guide (macOS)

This guide provides step-by-step instructions to set up and run the autonomous AI agent. The agent is highly flexible and can use various Large Language Models (LLMs) as its "brain."

## I. Core Setup (Required for All Modes)

1.  **Install Prerequisites via Homebrew:**
    ```bash
    brew install git python gh ollama
    ```

2.  **Authenticate with GitHub (Crucial Step):**
    This step authorizes the agent to push branches and create pull requests on your behalf. You must ensure you grant the correct permissions.

    **First, if you have logged in before, log out to be safe:**
    ```bash
    gh auth logout
    ```

    **Now, log in with the required permission scopes:**
    ```bash
    gh auth login --scopes repo,workflow
    ```
    -   When prompted, choose `HTTPS` as your preferred protocol.
    -   Follow the web browser authentication flow.
    -   **The `--scopes repo,workflow` part is essential.** It grants the token permission to push code and interact with repositories. Without this, the agent will fail with a "permission denied" error.

3.  **Install Python Libraries:**
    Navigate to the project's root directory and run:
    ```bash
    pip3 install -r requirements.txt
    ```

## II. Configuring LLM Providers (Choose one or more)

### Option A: Local LLM with Ollama (Recommended)
This method is free, private, and works offline. **Requires a Mac with 16GB+ RAM.**

1.  **Start the Ollama Service:** This command ensures Ollama is always running in the background.
    ```bash
    brew services start ollama
    ```
2.  **Download a Model:**
    ```bash
    ollama pull llama3 # Downloads the Llama 3 8B model (~4.7GB)
    ```
3.  **Model String for Agent:** `ollama/llama3`

### Option B: Cloud LLMs (OpenAI, Groq, Gemini)
These methods use powerful cloud APIs. They require API keys.

1.  **Create your `.env` file:**
    In the project root, copy the example file:
    ```bash
    cp .env.example .env
    ```
2.  **Get API Keys and Edit `.env`:**
    Open the new `.env` file and add your keys. You only need to add keys for the services you want to use.
    -   **OpenAI:** Get a key from [platform.openai.com/api-keys](https://platform.openai.com/api-keys).
        -   **Model String for Agent:** `gpt-4o` or `gpt-3.5-turbo`
    -   **Groq (for high-speed Llama 3 70B):** Get a key from [console.groq.com/keys](https://console.groq.com/keys).
        -   **Model String for Agent:** `groq/llama3-70b-8192`
    -   **Google Gemini:** Get a key from [aistudio.google.com](https://aistudio.google.com).
        -   **Model String for Agent:** `gemini/gemini-1.5-flash`

## III. Running the Agent

The agent is designed to be safe by default and does not have the ability to run arbitrary commands on your computer.

### Key Arguments:
-   `--model MODEL`: Specifies which LLM to use (e.g., `gpt-4o`). Defaults to `ollama/llama3`.
-   `--mode MODE`: `single` (runs one task cycle) or `continuous`. Defaults to `single`.

### Examples:

-   **Run one task with the default local model:**
    ```bash
    python3 scripts/run_local_agent.py
    ```

-   **Run one task with OpenAI's GPT-5:**
    ```bash
    python3 scripts/run_local_agent.py --model gpt-5
    ```

-   **Run continuously with Google's Gemini:**
    ```bash
    python3 scripts/run_local_agent.py --model gemini/gemini-2.5-pro
    ```

-   **Run continuously with Groq's high-speed Llama 3:**
    ```bash
    python3 scripts/run_local_agent.py --model groq/llama3-70b-8192 --mode continuous
    ```

-   **Run one task with Anthropic's Claude 4 Sonnet:**
    ```bash
    python3 scripts/run_local_agent.py --model claude-sonnet-4-20250514
    ```