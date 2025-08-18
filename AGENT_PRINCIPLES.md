# Autonomous Agent Principles

## 1. Terminology

-   **The Agent:** The Large Language Model (LLM) that provides the intelligence. The Agent analyzes the project context and makes all decisions about what actions to take.
-   **The Orchestrator:** The local Python script (`run_local_agent.py`) that the user executes. The Orchestrator is a simple, non-intelligent executor. Its only job is to provide context to the Agent and faithfully carry out the commands the Agent issues.

## 2. Core Principles

### 2.1 Specification-Driven
The Agent's primary directive is to fulfill tasks as defined in `TASKS.md`. It must adhere to all project specifications and guides when producing changes.

### 2.2 LLM-Led Intelligence
The Agent is the "brain." The Orchestrator is the "hands." The Orchestrator MUST NOT contain any logic for task selection, dependency checking, or any other decision-making process. All reasoning is delegated to the Agent.

### 2.3 Interactive Decision Points
When the Agent encounters an ambiguous situation that requires human input, it must use the `ask_question` tool to halt execution and present the user with a clear question. It must not make unsupervised architectural decisions.