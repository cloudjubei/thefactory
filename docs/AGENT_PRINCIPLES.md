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

## 3. Execution Principles

### 3.1 Single Feature Focus
The Agent must work on exactly ONE feature per execution cycle. This ensures:
- Complete context gathering for reliable decision-making
- Proper status tracking and progress visibility
- Thorough testing and validation
- Predictable and debuggable execution patterns

### 3.2 Context-First Approach
Before implementing any feature, the Agent must gather ALL required context:
- Read existing files that will be modified (never assume content)
- Retrieve all specification files referenced in the feature's Context field
- Examine related test files and dependency files
- Use the `ask_question` tool when context is insufficient or ambiguous

### 3.3 Test-Driven Completion
No feature is complete without passing tests:
- Create tests immediately after feature implementation
- Tests must verify each point in the feature's Acceptance criteria
- Use the `run_tests` tool to validate all tests pass
- Fix issues before marking features complete

### 3.4 Incremental Modification
When modifying existing files:
- Always read current content first
- Make minimal necessary changes
- Preserve existing functionality unless explicitly changing it
- Document the reasoning for changes