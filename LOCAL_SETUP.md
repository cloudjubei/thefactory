# Local Agent Setup and Usage Guide (macOS)

This guide provides step-by-step instructions to set up and run the autonomous AI agent. The agent is highly flexible and can use various Large Language Models (LLMs) as its "brain."

## I. Core Setup (Required for All Modes)
1.  **Install Prerequisites via Homebrew:**
    ```bash
    brew install git python gh ollama
    ```
2.  **Authenticate with GitHub:**
    ```bash
    gh auth login # Follow the prompts, selecting HTTPS
    ```
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

Use the `run_local_agent.py` script from your terminal.

### Key Arguments:
-   `--model`: Specifies which LLM to use. **Defaults to `ollama/llama3`**.
-   `--mode`: `single` (runs one task cycle) or `continuous` (runs until all tasks are done). **Defaults to `single`**.

### Examples:

-   **Run one task with the default local model:**
    ```bash
    python3 scripts/run_local_agent.py
    ```

-   **Run one task with OpenAI's GPT-4o:**
    ```bash
    python3 scripts/run_local_agent.py --model gpt-4o
    ```

-   **Run continuously with Groq's high-speed Llama 3:**
    ```bash
    python3 scripts/run_local_agent.py --model groq/llama3-70b-8192 --mode continuous
    ``````
---
**EXECUTION COMPLETE.**

All tasks are now complete. The agent is significantly more capable. It can run continuously, ask for help when it gets stuck, and can be easily configured to use a variety of powerful LLMs. The documentation is now comprehensive and accurate. The project is ready for you to run.