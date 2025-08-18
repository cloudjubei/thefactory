# Autonomous Agent Principles

## 1. Specification-Driven
The agent's primary directive is to fulfill tasks as defined in `TASKS.md`. It must adhere to all project specifications and guides when producing changes.

## 2. LLM-Led Intelligence (New Principle)
**The LLM is the agent.** The local Python script is merely an orchestrator. The orchestrator's sole responsibilities are:
-   To gather the full, unfiltered project context.
-   To present this context to the LLM.
-   To faithfully execute the file changes the LLM provides in its response.

The orchestrator **MUST NOT** contain logic for task selection, dependency checking, or any other "clever" behavior. All reasoning is delegated to the LLM.

## 3. Interactive Decision Points
(This principle remains unchanged)