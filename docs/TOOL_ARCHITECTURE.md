# Tool-Using Agent Architecture

## 1. Core Principle
The LLM is the agent. The local Python script is a simple, non-intelligent executor of the agent's commands. The agent's intelligence lies in its ability to select and sequence the correct "tools" to accomplish a task.

## 2. Agent-Orchestrator Contract
The agent (LLM) will communicate its intentions to the orchestrator (`run_local_agent.py`) via a structured JSON object. The orchestrator's only job is to parse this JSON and execute the specified tool calls.

## 3. JSON Response Schema
The LLM's response MUST be a single JSON object containing a `plan` and a list of `tool_calls`.

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
-  Description: Writes or overwrites a file with the given content.
-  Arguments:
   -  `path` (string): The relative path to the file.
   -  `content` (string): The full content to be written to the file.

### `retrieve_context_files`
-  Description: Reads and returns the content of the files at the given paths.
-  Arguments:
   -  `paths` (list[string]): Relative paths of files to retrieve.

### `rename_files`
-  Description: Safely rename or move files/directories within the repository. All paths are relative to the repository root. The tool prevents operations outside the repo and can operate in dry-run mode.
-  Arguments:
   -  `operations` (list[object], required): Each object has `from_path` (string) and `to_path` (string).
   -  `overwrite` (boolean, optional, default: false): Allow replacing existing destination files/directories.
   -  `dry_run` (boolean, optional, default: false): If true, validates and reports operations without making changes.
-  Returns: JSON string with keys: `ok` (bool), `summary` ({moved, skipped, errors}), `results` (list per operation with status and message).
-  Notes: This tool is implemented in `scripts/rename_files.py` and exposed to the agent via `AgentTools.rename_files` in `scripts/run_local_agent.py`.

### `run_tests`
-  Description: Execute the project's test suite (`scripts/run_tests.py`) and return a structured result.
-  Arguments: none
-  Returns: JSON string with keys: `ok` (bool), `exit_code` (int), `stdout` (str), `stderr` (str), `passed` (int|None), `total` (int|None).
-  Purpose: Enables the agent to verify acceptance criteria programmatically per feature and before submission.

### `finish_feature`
-  Description: Commit and push the current changes as a single "feature commit" with a standardized message.
-  Arguments:
   -  `task_id` (int): Parent task ID.
   -  `feature_id` (int): Feature index within the task (e.g., 10.1 -> 1).
   -  `title` (string): Short feature title used in the commit subject.
   -  `message` (string, optional): Longer description included in the commit body.
-  Behavior: Creates one commit per feature and pushes the current branch. Does not create a PR.

### `submit_for_review`
-  Description: A high-level tool that performs all the necessary steps to submit the agent's work. It automatically adds all file changes, commits them with a standardized message, and creates a pull request. This should be the final step in any successful plan.
-  Arguments:
   -  `task_id` (integer): The ID of the task being completed.
   -  `task_title` (string): The title of the task being completed.

### `ask_question`
-  Description: Use this tool ONLY when you encounter an ambiguous situation or a major, unspecified architectural decision that requires human input. This tool will halt execution and display your question to the user.
-  Arguments:
   -  `question_text` (string): The clear, concise question for the user.

### `finish`
-  Description: A special tool to indicate that the agent's work is complete for this cycle. Use it after creating a pull request or when no eligible tasks are found. In continuous mode, the orchestrator will start a new cycle after this tool is called.

## 5. Execution Modes
-  Single Mode: The orchestrator will execute one plan (one set of tool calls from the LLM) and then exit.
-  Continuous Mode: The orchestrator will execute a plan. If the plan ends with `finish`, it will re-clone the repository to get the latest state and start a new cycle by asking the agent for the next plan. The loop terminates only if the agent calls `ask_question` or if the `finish` tool is called because no tasks were found.

## 6. Mandatory Task Completion Workflow
To be considered complete, any plan that successfully addresses a task MUST conclude with the following sequence of tool calls. This is the agent's "definition of done."

1.  `write_file`: All file modifications, including updating the relevant task's status in `TASKS.md`.
2.  `submit_for_review`: To package and submit all changes for human review.
3.  `finish`: To signal the successful completion of the work cycle.

Per-feature completion: After implementing and testing each feature, the agent must call `finish_feature` to create an isolated commit before proceeding to the next feature.
