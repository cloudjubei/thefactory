# LLM Integration Specification

## 1. Problem Statement
The agent's execution logic must be elevated from a simple, rule-based automaton to an intelligent system capable of reasoning about and completing novel tasks. This will be achieved by integrating a Large Language Model (LLM) to act as the agent's "brain." This document specifies the contract between the local Python orchestrator and the LLM service.

## 2. Core Workflow
1.  **Context Gathering:** The local orchestrator reads the selected task and relevant project files.
2.  **Prompt Construction:** A detailed, structured prompt is assembled from the gathered context.
3.  **API Call:** The prompt is sent to the designated LLM API.
4.  **Response Parsing:** The LLM's response, which must be in a specific format, is parsed by the orchestrator.
5.  **File System Action:** The orchestrator writes the files and makes the changes described in the parsed response.

## 3. Context Gathering
The following files **MUST** be read and included in the prompt to provide the LLM with sufficient context about the project's goals and standards:
- `SPEC.md`
- `SPECIFICATION_GUIDE.md`
- `TASK_FORMAT.md`
- `TASKS.md` (The full contents)

The specific task to be executed (ID, Title, Action, Acceptance) is the primary focus and must be clearly delimited in the prompt.

## 4. Prompt Structure
The prompt sent to the LLM must adhere to the following structure:

You are an autonomous AI agent expert in software engineering and specification-driven development. Your goal is to complete a single task within a given project.

PROJECT CONTEXT
Here are the core documents that define the project's philosophy and standards. Adhere to them strictly.

--- START of SPEC.md ---
[Contents of SPEC.md]
--- END of SPEC.md ---

--- START of SPECIFICATION_GUIDE.md ---
[Contents of SPECIFICATION_GUIDE.md]
--- END of SPECIFICATION_GUIDE.md ---

--- START of TASK_FORMAT.md ---
[Contents of TASK_FORMAT.md]
--- END of TASK_FORMAT.md ---

CURRENT TASK LIST
This is the full list of tasks. Your assigned task is clearly marked below.

--- START of TASKS.md ---
[Contents of TASKS.md]
--- END of TASKS.md ---

YOUR ASSIGNED TASK
You must complete the following task:

ID: [Task ID]
Title: [Task Title]
Action: [Task Action Description]
Acceptance Criteria: [Task Acceptance Criteria]

INSTRUCTIONS
Analyze the request and create or modify the necessary files to meet the Acceptance Criteria.

Your response MUST be a single Markdown block.

For each file you need to create or modify, use a Markdown code block with the full file path.

The content inside each block will be written directly to the file.

If you do not need to modify a file, do not include it in your response.

Example Response Format:

´ ´ ´markdown ´ ´ ´[path/to/file1.md]

This is the new content for file1
This file has been created to meet the task requirements.
` ´ ´ ´

` ´ ´ ´[path/to/another/file.py]

This is a python script
print("Hello, World!")
´ ´ ´ ´ ´ ´

Now, generate the response to complete your assigned task.


## 5. API Key Management
The API key for the LLM service **MUST NOT** be hardcoded. The local orchestrator will read the key from an environment variable named `GEMINI_API_KEY`. If this variable is not set, the script must exit with a clear error message.

## 6. Response Parsing
The local orchestrator is responsible for parsing the LLM's Markdown response. It will use regular expressions to find all code blocks annotated with a file path (`´´´[file/path]`). It will then extract the content of each block and write it to the corresponding file path within the cloned repository.

