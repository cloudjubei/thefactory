
import os
import re
import sys
import argparse
import subprocess
import json
import litellm
from dotenv import load_dotenv
from git_manager import GitManager

# --- AGENT TOOLS ---
class AgentTools:
    def __init__(self, repo_path: str, git_manager: GitManager):
        self.repo_path = repo_path
        self.git_manager = git_manager

    def write_file(self, path: str, content: str):
        full_path = os.path.join(self.repo_path, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as f:
            f.write(content)
        return f"Successfully wrote {len(content)} bytes to {path}"

    def run_shell_command(self, command: str):
        # SECURITY: This is a powerful tool. In a real-world scenario,
        # this would need significant sandboxing and validation.
        # For this project, we trust the LLM's output.
        result = subprocess.run(command, shell=True, cwd=self.repo_path, capture_output=True, text=True)
        if result.returncode != 0:
            return f"Error executing command: {command}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        return f"Successfully executed command: {command}\nSTDOUT:\n{result.stdout}"

    def create_pull_request(self, title: str, body: str):
        if self.git_manager.create_pull_request(title, body):
            return "Pull request created successfully."
        return "Failed to create pull request."

    def finish(self, reason: str):
        return f"Agent finished. Reason: {reason}"

# --- UNIFIED LLM ENGINE ---
class UnifiedEngine:
    def generate_plan_and_tool_calls(self, model: str, context: dict) -> list:
        messages = self._build_prompt(context)
        response_text = self._make_api_call(model, messages)
        return self._parse_response(response_text)

    def _build_prompt(self, context: dict) -> list:
        context_str = ""
        for name, content in context.items():
            context_str += f"--- START of {name} ---\n{content}\n--- END of {name} ---\n\n"

        system_prompt = """
You are an autonomous AI agent. Your goal is to advance a software project by completing one task.
You operate by generating a plan and a sequence of tool calls in a single JSON response.
You have access to the following tools:
- `write_file(path, content)`: Writes or overwrites a file.
- `run_shell_command(command)`: Executes a shell command (e.g., for git).
- `create_pull_request(title, body)`: Creates a pull request.
- `finish(reason)`: Stops execution.

Your process is:
1. Analyze the project context and `TASKS.md`.
2. Identify the lowest-ID pending task (`-`) whose dependencies are met (`+`).
3. Formulate a plan to complete this task.
4. Generate the sequence of tool calls to execute your plan. This includes:
   a. Writing new files or modifying existing ones (`write_file`).
   b. Updating the task status in `TASKS.md` from `-` to `~` (`write_file`).
   c. Adding your changes to git (`run_shell_command` with `git add`).
   d. Committing your changes (`run_shell_command` with `git commit`).
   e. Creating the pull request (`create_pull_request`).
   f. Concluding with `finish`.

If no tasks are eligible, your ONLY tool call should be `finish(reason="HALT: No eligible tasks found.")`.
Respond with a single JSON object. Do not add any other text.
"""
        user_prompt = f"### PROJECT CONTEXT\n{context_str}\n\nGenerate the JSON response to complete the next task."
        return [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}]

    def _make_api_call(self, model: str, messages: list) -> str:
        print(f"Sending prompt to model '{model}' via LiteLLM...")
        try:
            response = litellm.completion(model=model, messages=messages, timeout=300, response_format={"type": "json_object"})
            if response.choices and response.choices[0].message:
                return response.choices[0].message.content or ""
            return ""
        except Exception as e:
            print(f"Error: API call via LiteLLM failed: {e}", file=sys.stderr)
            sys.exit(1)

    def _parse_response(self, response: str) -> list:
        print("\n--- LLM Response Received ---\n")
        print(response)
        try:
            # Clean the response to ensure it's valid JSON
            json_str = response.strip()
            if json_str.startswith("```json"):
                json_str = json_str[7:-4].strip()
            
            data = json.loads(json_str)
            print("\n--- Agent's Plan ---")
            print(data.get("plan", "No plan provided."))
            return data.get("tool_calls", [])
        except json.JSONDecodeError as e:
            print(f"Error: Failed to decode LLM response as JSON: {e}", file=sys.stderr)
            print(f"Raw Response:\n{response}", file=sys.stderr)
            return []

# --- AGENT ORCHESTRATOR ---
class Agent:
    def __init__(self, model: str):
        self.model = model
        self.engine = UnifiedEngine()
        # Git manager is initialized later after cloning
        self.git_manager = None
        self.tools = None

    def run_single_task(self):
        print(f"--- Starting Agent ---")
        
        # Setup temporary repo for the agent to work in
        repo_url = self._get_repo_url()
        self.git_manager = GitManager(repo_url=repo_url)
        # We need a branch from the start, but the agent will decide the name later
        if not self.git_manager.setup_repository(branch_name="agent/work-in-progress"): return

        # Initialize tools with the correct context
        self.tools = AgentTools(self.git_manager.repo_path, self.git_manager)
        
        context = self._gather_context()
        tool_calls = self.engine.generate_plan_and_tool_calls(self.model, context)

        if not tool_calls:
            print("Agent halted. The LLM did not return any tool calls.")
            return

        self._execute_tool_calls(tool_calls)
        
        # The agent is expected to call `create_pull_request` itself now.
        # The final `finish` call will stop the loop.

    def _execute_tool_calls(self, tool_calls: list):
        print("\n--- Executing Tool Calls ---")
        for call in tool_calls:
            tool_name = call.get("tool_name")
            arguments = call.get("arguments", {})
            
            tool_method = getattr(self.tools, tool_name, None)
            
            if not tool_method:
                print(f"Error: Unknown tool '{tool_name}'")
                continue

            print(f"Calling Tool: {tool_name}({arguments})")
            try:
                result = tool_method(**arguments)
                print(f"Tool Result: {result}")
                if tool_name == 'finish':
                    print("--- Agent execution complete. ---")
                    return # Stop execution
            except Exception as e:
                print(f"Error executing tool '{tool_name}': {e}")


    def _gather_context(self):
        # We now gather context from the temporary clone so the agent has the latest info
        files = ["SPEC.md", "SPECIFICATION_GUIDE.md", "TASK_FORMAT.md", "TASKS.md", "AGENT_PRINCIPLES.md"]
        context = {}
        for filename in files:
            try:
                with open(os.path.join(self.git_manager.repo_path, filename), "r") as f:
                    context[filename] = f.read()
            except FileNotFoundError:
                print(f"Warning: Context file not found: {filename}")
        return context

    def _get_repo_url(self):
        try:
            result = subprocess.run(
                ["git", "config", "--get", "remote.origin.url"],
                check=True, capture_output=True, text=True
            )
            url = result.stdout.strip()
            if url.startswith("git@"): url = url.replace(":", "/").replace("git@", "https://")
            return url + ".git" if not url.endswith(".git") else url
        except subprocess.CalledProcessError:
            print("Error: Could not determine git remote URL.", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser(description="Autonomous AI Agent for Specification Programming.")
    parser.add_argument('--model', type=str, default='ollama/llama3',
                        help="The model string via LiteLLM (e.g., 'ollama/llama3'). (Default: ollama/llama3)")
    args = parser.parse_args()
    
    agent = Agent(model=args.model)
    agent.run_single_task()