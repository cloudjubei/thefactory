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