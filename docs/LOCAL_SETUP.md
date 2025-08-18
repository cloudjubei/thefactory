# Local Setup Guide

This guide details the steps to set up the project locally and run the autonomous AI agent.

## Prerequisites

Before you begin, ensure you have the following installed:

*   **Git**: For cloning the repository.
*   **Python 3.8+**: The agent and its tools are written in Python.
*   **(Optional) Docker / Ollama**: If you plan to run local LLMs like Llama3 via Ollama.

## 1. Clone the Repository

First, clone the project repository to your local machine:

```bash
git clone <repository_url>
cd <project_directory>
```

## 2. Set Up a Python Virtual Environment

It is highly recommended to use a virtual environment to manage dependencies.

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

## 3. Install Dependencies

Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

## 4. Configure Environment Variables

Some functionalities, especially interacting with Large Language Models (LLMs), may require API keys or specific configurations. Copy the `.env.example` file to `.env` and populate it with your actual values.

```bash
cp .env.example .env
```

Edit the newly created `.env` file:

```ini
# .env
# Example: For OpenAI models
# OPENAI_API_KEY="sk-YOUR_OPENAI_API_KEY"

# Example: For local Ollama setup if using a non-default port or host
# LITELLM_BASE_URL="http://localhost:11434"
```

## 5. Running the Agent

The agent's orchestrator script is `scripts/run_local_agent.py`.

### Basic Execution

To run the agent in 'single' mode (executes one cycle and exits):

```bash
python scripts/run_local_agent.py --mode single
```

### Specifying an LLM Model

You can specify the LLM model using the `--model` argument. LiteLLM supports a wide range of models and providers (e.g., `ollama/llama3`, `gpt-4`, `claude-3-opus-20240229`).

```bash
python scripts/run_local_agent.py --mode single --model ollama/llama3
# Or for OpenAI:
# python scripts/run_local_agent.py --mode single --model gpt-4
```

### Continuous Mode

In 'continuous' mode, the agent will automatically re-clone the repository to get the latest state and start a new cycle after completing a task or `finish`ing its current work. It will continue until it calls `ask_question` or `finish` with no eligible tasks found.

```bash
python scripts/run_local_agent.py --mode continuous --model ollama/llama3
```

### Important Notes

*   **Safety**: The agent runs in a safe mode, restricted to its repository. It will not execute commands outside the project directory.
*   **Review**: All changes made by the agent are submitted as a pull request for human review. Always review generated code before merging.