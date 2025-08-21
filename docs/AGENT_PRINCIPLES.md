# Agent Core Principles

This document outlines the fundamental principles that govern the agent's behavior, decision-making, and development workflow. These principles ensure that the agent operates in a predictable, reliable, and effective manner.

## 1. Task-Driven
The agent's work is exclusively driven by tasks defined in the `tasks/` directory. Each task is broken down into a series of discrete, verifiable features. The agent must always work within the scope of a single feature at a time.

## 2. Specification-Led
The agent must adhere to the specifications and guidelines defined in the `docs/` directory. These documents are the canonical source of truth for the project's architecture, tooling, and processes. Key specifications include:
- `docs/PLAN_SPECIFICATION.md`: How to structure and execute plans.
- `docs/TESTING.md`: How to write and run tests.
- `docs/TOOL_ARCHITECTURE.md`: The contract for available tools.

## 3. Test-Verified
All tangible outputs produced by the agent must be verifiable by deterministic, automated tests. A feature is not considered complete until its corresponding tests pass, confirming that its acceptance criteria have been met.

## 4. Incremental and Atomic Progress
The agent makes progress through small, incremental changes. Each feature is completed and committed as a single, atomic unit of work using the `finish_feature` tool. This ensures a clean, auditable history of changes.

## 5. Autonomous Operation
The agent is designed to be autonomous. It should be able to interpret tasks, create plans, write code, run tests, and submit its work for review with minimal human intervention. The `ask_question` tool should only be used for significant ambiguities that block progress.

## 6. Structured Communication
The agent communicates its intentions and actions through a strict JSON schema. This contract with the orchestrator ensures that its behavior is predictable and that its tool usage can be reliably executed and monitored. The primary communication artifact is the JSON response containing the `plan` and `tool_calls`.