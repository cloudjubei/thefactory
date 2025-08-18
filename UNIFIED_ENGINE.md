# Unified LLM Engine Specification

## 1. Problem Statement
The previous agent architecture was brittle, requiring provider-specific code for each LLM. To make the agent more robust, extensible, and maintainable, it will be refactored to use a single, unified execution engine powered by the `LiteLLM` library.

## 2. Core Technology
- **`LiteLLM`:** This Python library provides a standardized, OpenAI-compatible interface for making calls to over 100 LLM providers, including Ollama (local) and Gemini (cloud). It will be the sole interface for all LLM communication.

## 3. Dependency Management
- All required Python libraries will be listed in a `requirements.txt` file in the project root.
- Users will install these dependencies using `pip3 install -r requirements.txt`.

## 4. API Key and Configuration Management
- API keys **MUST NOT** be stored in code.
- A `.env.example` file will be provided in the project root to template required environment variables.
- Users will be instructed to copy this file to `.env` and fill in their own keys.
- The agent will use the `python-dotenv` library to load these variables at runtime.

## 5. Agent Control
The agent's CLI will be simplified.

-   **`--model MODEL_STRING`**: This argument replaces `--provider`. The user can pass any model string supported by `LiteLLM`.
    -   Default: `ollama/llama3`
    -   Example for cloud: `gemini/gemini-1.5-flash`
-   **`--mode {single,continuous}`**: This argument remains unchanged.

## 6. Architecture
- The `OllamaEngine` and `GeminiEngine` classes will be removed.
- They will be replaced by a single `UnifiedEngine` class whose `_make_api_call` method consists of a single, standardized call to `litellm.completion()`.