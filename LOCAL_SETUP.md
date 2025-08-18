# Local Agent Setup and Usage Guide (macOS)
...
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

-   **Run one task with OpenAI's GPT-4o:**
    ```bash
    python3 scripts/run_local_agent.py --model gpt-4o
    ```

-   **Run continuously with Groq's high-speed Llama 3:**
    ```bash
    python3 scripts/run_local_agent.py --model groq/llama3-70b-8192 --mode continuous
    ``````
---
**COMPLETION NOTICE:** Task 15 is complete. The agent has been fundamentally re-architected to be safer and more effective. The dangerous `run_shell_command` tool has been completely removed and replaced with a high-level `submit_for_review` tool, and all related safety flags and documentation have been updated. The agent is now ready for you to run.