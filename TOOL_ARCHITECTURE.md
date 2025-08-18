# Tool-Using Agent Architecture

## 1. Core Principle
The LLM is the agent. The local Python script is a simple, non-intelligent executor of the agent's commands. The agent's intelligence lies in its ability to select and sequence the correct "tools" to accomplish a task.

## 2. Agent-Orchestrator Contract
The agent (LLM) will communicate its intentions to the orchestrator (`run_local_agent.py`) via a structured JSON object. The orchestrator's only job is to parse this JSON and execute the specified tool calls.

## 3. JSON Response Schema
The LLM's response **MUST** be a single JSON object containing a `plan` and a list of `tool_calls`.

**Schema:**
```json
{
  "plan": "A short, high-level, step-by-step plan of what the agent intends to do.",
  "tool_calls": [
    {
      "tool_name": "name_of_the_tool_to_use",
      "arguments": {
        "arg1_name": "value1",
        "arg2_name": "value2"
      }
    }
  ]
}
```

## 4. Available Tools
The orchestrator will make the following Python functions available as tools to the LLM.

### `write_file`
-   **Description:** Writes or overwrites a file with the given content.
-   **Arguments:**
    -   `path` (string): The relative path to the file.
    -   `content` (string): The full content to be written to the file.

### `run_shell_command`
-   **Description:** Executes a shell command in the root of the temporary repository clone. Use this for git operations like git add and git commit.
-   **Arguments:**
    -   `command` (string): The exact shell command to execute.
Security Note: This tool is powerful. The orchestrator must handle it with care, but for this project, we trust the agent's output.

### `create_pull_request`
-   **Description:** Creates a pull request on GitHub for the changes that have been staged and committed. This should be the final step in any plan.
-   **Arguments:**
    -   `title` (string): The title of the pull request.
    -   `body` (string): The body/description of the pull request.

### `ask_question`
-   **Description:** Use this tool ONLY when you encounter an ambiguous situation or a major, unspecified architectural decision that requires human input. This tool will halt execution and display your question to the user.
-   **Arguments:**
    -   `question_text` (string): The clear, concise question for the user.

### `finish`
-   **Description:** A special tool to indicate that the agent's work is complete for this cycle. Use it after creating a pull request or when no eligible tasks are found. **In continuous mode, the orchestrator will start a new cycle after this tool is called.**

## 5. Safety and Dangerous Tools

To ensure user safety, the agent operates in **Safe Mode** by default.

### 5.1 Tool Categories
Tools are categorized as either `safe` or `dangerous`.
-   **Safe Tools:** These tools operate within a limited scope and do not grant arbitrary code execution.
    -   `write_file`
    -   `create_pull_request`
    -   `ask_question`
    -   `finish`
-   **Dangerous Tools:** These tools can have wide-ranging effects on the user's system.
    -   `run_shell_command`

### 5.2 Safe Mode (Default)
-   By default, the agent runs with dangerous tools disabled.
-   The orchestrator **MUST NOT** include any dangerous tools in the system prompt sent to the LLM. The LLM will be unaware that these tools exist.
-   If the LLM attempts to call a dangerous tool (e.g., through hallucination), the orchestrator **MUST** reject the call.

### 5.3 Enabling Dangerous Tools
-   The user can disable Safe Mode by providing the `--allow-dangerous-tools` command-line flag.
-   Only when this flag is present will the orchestrator include dangerous tools in the system prompt.

## 6. Execution Modes
-   **Single Mode:** The orchestrator will execute one plan (one set of tool calls from the LLM) and then exit.
-   **Continuous Mode:** The orchestrator will execute a plan. If the plan ends with `finish`, it will re-clone the repository to get the latest state and start a new cycle by asking the agent for the next plan. The loop terminates only if the agent calls `ask_question` or if the `finish` tool is called because no tasks were found.