# Agent Architecture Specification

## 1. Core Design
The agent will be architected in a modular fashion to separate concerns:
- **Orchestrator (`Agent` class):** The main controller responsible for parsing tasks, managing the execution loop, and interacting with the file system and Git.
- **Execution Engine (e.g., `OllamaEngine`, `GeminiEngine`):** A swappable "brain." Each engine is responsible for communicating with a specific LLM backend.

## 2. Command-Line Interface (CLI)
The user will control the agent via command-line arguments.

**Usage:** `python3 scripts/run_local_agent.py [options]`

### Arguments:
-   **`--provider {local,cloud}`**
    -   **Description:** Selects the LLM provider to use.
    -   **`local`:** Uses the Ollama engine. Assumes an Ollama server is running locally. (Default)
    -   **`cloud`:** Uses the Gemini engine. Requires the `GEMINI_API_KEY` environment variable.
-   **`--mode {single,continuous}`**
    -   **Description:** Determines the execution behavior.
    -   **`single`:** The agent finds and executes the next single available task, then exits. (Default)
    -   **`continuous`:** The agent executes all available tasks in a loop until no pending tasks with met dependencies remain, then exits.

## 3. LLM Engine API Contract
All execution engines must conform to a standard interface. They will be initialized and then a method `execute_task(task_details, context_files)` will be called.

-   **Input:**
    -   `task_details`: A dictionary containing the ID, title, action, etc., of the task.
    -   `context_files`: A dictionary mapping filenames to their full string content.
-   **Output:** The method must return a dictionary mapping file paths to their new string content. `{'path/to/file.py': 'new_content', ...}`

This ensures the main orchestrator can use any engine without knowing its internal implementation details.