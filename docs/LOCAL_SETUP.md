# Local Setup Guide

This document provides step-by-step instructions for setting up the local development environment and running the AI agent orchestrator.

## 1. Prerequisites

Before you begin, ensure you have the following installed on your system:

-   **Python 3.8 or higher**: [Download Python](https://www.python.org/downloads/)
-   **Git**: [Download Git](https://git-scm.com/downloads)

## 2. Setup Instructions

Follow these steps to get the project running.

### Step 2.1: Clone the Repository

First, clone the project repository to your local machine using Git.

```bash
git clone <your_repository_url>
cd <repository_directory>
```

### Step 2.2: Create a Python Virtual Environment
It is highly recommended to use a virtual environment to manage project dependencies and avoid conflicts with other Python projects.
# Create the virtual environment
`python3 -m venv venv`

# Activate the virtual environment
# On macOS and Linux:
source venv/bin/activate

# On Windows:
`.\venv\Scripts\activate`

You will know the environment is active when you see (venv) at the beginning of your command prompt.

### Step 2.3: Install Dependencies
With the virtual environment active, install the required Python packages using the requirements.txt file.
```pip install -r requirements.txt```

### Step 2.4: Configure Environment Variables
The agent requires API keys to connect to LLM services. These are managed through a .env file.
1. Copy the example file to create your own configuration:
```cp .env.example .env```
2. Open the newly created .env file in a text editor.
3. Add your API key for the LLM provider you intend to use. For example, to use OpenAI's models, you would set:
```OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"```

### Step 3. Running the Agent

The primary script for running the agent is scripts/run_local_agent.py. It orchestrates the interaction between the LLM and the project's tools.
Command-Line Arguments
The script accepts the following arguments:
Argument	Required	Description	Example
--model	No	The model name to use, as recognized by litellm.	gpt-4-turbo
--agent	Yes	The agent persona to activate (planner, tester, or developer).	developer
--task	Yes	The numeric ID of the task to work on, corresponding to a directory in tasks/.	2
--feature	No	The specific feature ID to work on. If omitted, the script automatically picks the next pending feature.	2.3
--mode	No	The execution mode: single (runs until finish_feature) or continuous (runs until finish).	single
Example Command
To run the developer agent on task 2, using the gpt-4-turbo model, and have it automatically pick the next pending feature: