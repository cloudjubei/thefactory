# scripts/run_local_agent.py

import os
import re
import sys
import argparse
import subprocess
import json
import litellm
from dotenv import load_dotenv
from git_manager import GitManager

# --- TOOL REGISTRY AND SAFETY ---
TOOL_REGISTRY = {
    "write_file": {"function_name": "write_file", "dangerous": False},
    "create_pull_request": {"function_name": "create_pull_request", "dangerous": False},
    "ask_question": {"function_name": "ask_question", "dangerous": False},
    "finish": {"function_name": "finish", "dangerous": False},
    "run_shell_command": {"function_name": "run_shell_command", "dangerous": True},
}

class AgentTools:
    def __init__(self, repo_path: str, git_manager: GitManager):
        self.repo_path = repo_path
        self.git_manager = git_manager
    def write_file(self, path: str, content: str):
        full_path = os.path.join(self.repo_path, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as f: f.write(content)
        return f"Successfully wrote {len(content)} bytes to {path}"
    def run_shell_command(self, command: str):
        result = subprocess.run(command, shell=True, cwd=self.repo_path, capture_output=True, text=True)
        if result.returncode != 0: return f"Error: {result.stderr}"
        return f"Success: {result.stdout}"
    def create_pull_request(self, title: str, body: str):
        if self.git_manager.create_pull_request(title, body): return "Pull request created successfully."
        return "Failed to create pull request."
    def ask_question(self, question_text: str):
        return f"HALT: Agent has a question: {question_text}"
    def finish(self, reason: str):
        return f"Agent finished cycle. Reason: {reason}"

# --- UNIFIED LLM ENGINE ---
class UnifiedEngine:
    def generate_plan_and_tool_calls(self, model: str, context: dict, available_tools: list) -> list:
        messages = self._build_prompt(context, available_tools)
        response_text = self._make_api_call(model, messages)
        return self._parse_response(response_text)

    def _build_prompt(self, context: dict, available_tools: list) -> list:
        context_str = "\n".join(f"--- START of {name} ---\n{content}\n--- END of {name} ---\n" for name, content in context.items())
        tool_descriptions = {
            "write_file": "`write_file(path, content)`: Writes or overwrites a file.",
            "create_pull_request": "`create_pull_request(title, body)`: Creates a pull request.",
            "ask_question": "`ask_question(question_text)`: Halts all work and asks the user a question.",
            "finish": "`finish(reason)`: Stops the current work cycle.",
            "run_shell_command": "`run_shell_command(command)`: Executes a shell command (e.g., for git)."
        }
        tools_list_str = "\n".join(f"- {tool_descriptions[tool]}" for tool in available_tools)
        system_prompt = f"""
You are an autonomous AI agent. Your goal is to advance a software project by completing one task.
You operate by generating a plan and a sequence of tool calls in a single JSON response.
You have access to the following tools:
{tools_list_str}
Your process:
1. Analyze the context and `TASKS.md`.
2. Identify the next pending task.
3. Formulate a plan and the sequence of tool calls to complete it, ending with `finish`.
4. If no tasks are eligible, call `finish(reason="HALT: No eligible tasks found.")`.
Respond with a single JSON object.
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
            json_str = response.strip()
            if json_str.startswith("```json"): json_str = json_str[7:-4].strip()
            data = json.loads(json_str)
            print("\n--- Agent's Plan ---")
            print(data.get("plan", "No plan provided."))
            return data.get("tool_calls", [])
        except json.JSONDecodeError as e:
            print(f"Error: Failed to decode LLM response as JSON: {e}", file=sys.stderr)
            return []

# --- AGENT ORCHESTRATOR ---
class Agent:
    def __init__(self, model: str, mode: str, allow_dangerous: bool):
        self.model = model
        self.mode = mode
        self.allow_dangerous = allow_dangerous
        self.engine = UnifiedEngine()
        self.available_tools = self._get_available_tools()
        print(f"Agent initialized. Mode: {self.mode}, Dangerous tools allowed: {self.allow_dangerous}")

    def _get_available_tools(self) -> list:
        return [name for name, details in TOOL_REGISTRY.items() if not details["dangerous"] or self.allow_dangerous]

    def run(self):
        run_count = 0
        while True:
            run_count += 1
            print(f"\n--- Starting Cycle {run_count} ---")
            
            # ** THE FIX IS HERE (Part 1/2) **
            # We pass `run_count` as an argument.
            should_continue = self._execute_cycle(run_count)
            
            if not should_continue or self.mode == 'single':
                break
        print("\n--- Agent has finished all work. ---")

    # ** THE FIX IS HERE (Part 2/2) **
    # The method now accepts `run_count`.
    def _execute_cycle(self, run_count: int) -> bool:
        repo_url = self._get_repo_url()
        git_manager = GitManager(repo_url=repo_url)
        
        if not git_manager.setup_repository(branch_name=f"agent/cycle-{run_count}"):
            return False

        tools_instance = AgentTools(git_manager.repo_path, git_manager)
        context = self._gather_context(git_manager.repo_path)
        tool_calls = self.engine.generate_plan_and_tool_calls(self.model, context, self.available_tools)

        if not tool_calls:
            print("Agent halted. No tool calls returned.")
            return False

        return self._execute_tool_calls(tools_instance, tool_calls)

    def _execute_tool_calls(self, tools_instance: AgentTools, tool_calls: list) -> bool:
        print("\n--- Executing Tool Calls ---")
        for call in tool_calls:
            tool_name = call.get("tool_name")
            arguments = call.get("arguments", {})
            if tool_name not in self.available_tools:
                print(f"Error: Agent attempted to call disallowed tool '{tool_name}'. Halting.")
                return False
            tool_method = getattr(tools_instance, tool_name, None)
            if not tool_method:
                print(f"Error: Unknown tool implementation '{tool_name}'.")
                continue
            print(f"Calling Tool: {tool_name}({arguments})")
            try:
                result = tool_method(**arguments)
                print(f"Tool Result: {result}")
                if tool_name in ['ask_question', 'finish'] and "HALT" in result:
                    return False
            except Exception as e:
                print(f"Error executing tool '{tool_name}': {e}")
                return False
        return True

    def _gather_context(self, repo_path: str):
        files = ["SPEC.md", "SPECIFICATION_GUIDE.md", "TASK_FORMAT.md", "TASKS.md", "AGENT_PRINCIPLES.md"]
        context = {}
        for filename in files:
            try:
                with open(os.path.join(repo_path, filename), "r") as f:
                    context[filename] = f.read()
            except FileNotFoundError:
                pass
        return context

    def _get_repo_url(self):
        try:
            result = subprocess.run(["git", "config", "--get", "remote.origin.url"], check=True, capture_output=True, text=True)
            url = result.stdout.strip()
            if url.startswith("git@"): url = url.replace(":", "/").replace("git@", "https://")
            return url + ".git" if not url.endswith(".git") else url
        except subprocess.CalledProcessError:
            print("Error: Could not determine git remote URL.", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser(description="Autonomous AI Agent for Specification Programming.")
    parser.add_argument('--model', type=str, default='ollama/llama3', help="The LiteLLM model string.")
    parser.add_argument('--mode', choices=['single', 'continuous'], default='single', help="Execution mode.")
    parser.add_argument('--allow-dangerous-tools', action='store_true', help="Allow the agent to use dangerous tools like `run_shell_command`.")
    args = parser.parse_args()
    
    agent = Agent(model=args.model, mode=args.mode, allow_dangerous=args.allow_dangerous_tools)
    agent.run()