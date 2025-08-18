import os
import re
import sys
import argparse
import subprocess
import json
import litellm
from dotenv import load_dotenv
from git_manager import GitManager
from scripts.tools.write_file import write_file_tool
from scripts.tools.retrieve_context_files import retrieve_context_files_tool
from scripts.tools.rename_files import rename_files as rename_files_tool
from scripts.tools.submit_for_review import submit_for_review_tool
from scripts.tools.ask_question import ask_question_tool
from scripts.tools.finish import finish_tool

class AgentTools:
    def __init__(self, repo_path: str, git_manager: GitManager):
        self.repo_path = repo_path
        self.git_manager = git_manager

    def write_file(self, path: str, content: str):
        return write_file_tool(self.repo_path, path, content)

    def retrieve_context_files(self, paths: list):
        return retrieve_context_files_tool(self.repo_path, paths)

    def rename_files(self, operations: list, overwrite: bool = False, dry_run: bool = False):
        try:
            return json.dumps(rename_files_tool(operations=operations, base_dir=self.repo_path, overwrite=overwrite, dry_run=dry_run))
        except Exception as e:
            return json.dumps({"ok": False, "error": f"Failed to execute rename_files tool: {e}"})

    def submit_for_review(self, task_id: int, task_title: str):
        return submit_for_review_tool(self.git_manager, task_id, task_title)

    def ask_question(self, question_text: str):
        return ask_question_tool(question_text)

    def finish(self, reason: str):
        return finish_tool(reason)

class UnifiedEngine:
    def generate_plan_and_tool_calls(self, model: str, context: dict, task_id: int = None, feature_id: int = None) -> list:
        messages = self._build_prompt(context, task_id, feature_id)
        response_text = self._make_api_call(model, messages)
        return self._parse_response(response_text)

    def _build_prompt(self, context: dict, task_id: int = None, feature_id: int = None) -> list:
        context_str = "\n".join(f"--- START of {name} ---\n{content}\n--- END of {name} ---\n" for name, content in context.items())
        
        system_prompt = f"""
You are an autonomous AI agent. Your goal is to advance a software project by completing one task.
You operate by generating a plan and a sequence of tool calls in a single JSON response.

You have access to the following SAFE tools:
- `write_file(path, content)`
- `retrieve_context_files(paths: list)`
- `rename_files(operations: list, overwrite: bool, dry_run: bool)`
- `submit_for_review(task_id, task_title)`
- `ask_question(question_text)`
- `finish(reason)`

**YOUR JSON RESPONSE MUST follow this schema precisely:**
{{
  "plan": "Your high-level plan...",
  "tool_calls": [
    {{
      "tool_name": "name_of_tool",
      "arguments": {{ "arg_name": "value" }}
    }}
  ]
}}
The key for a tool's parameters MUST be "arguments".

**YOUR WORKFLOW IS MANDATORY:**
1.  Analyze the context to identify the next eligible pending task.
2.  Formulate a plan to complete the task.
3.  Generate `tool_calls` to:
    a.  `write_file` for all necessary changes.
    b.  `write_file` to update the task's status in `TASKS.md`.
    c.  `submit_for_review` with the correct `task_id` and `task_title`.
    d.  `finish` to end the cycle.

If no tasks are eligible, your ONLY tool call is `finish(reason=\"HALT: No eligible tasks found.\")`.
Respond with a single, valid JSON object.
"""
        user_prompt_parts = ["### PROJECT CONTEXT"]
        user_prompt_parts.append(context_str)

        if task_id:
            specific_task_instruction = f"You are instructed to work on Task {task_id}."
            if feature_id:
                specific_task_instruction += f" Specifically, focus on Feature {task_id}.{feature_id} within this task."
            specific_task_instruction += " Ignore the '1. Analyze the context to identify the next eligible pending task.' step and directly formulate a plan and tool calls for this specific task/feature."
            user_prompt_parts.append(specific_task_instruction)
            user_prompt_parts.append("\nGenerate the JSON response to complete the specified task/feature.")
        else:
            user_prompt_parts.append("\nGenerate the JSON response to complete the next task.")
        
        user_prompt = "\n".join(user_prompt_parts)
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

class Agent:
    def __init__(self, model: str, mode: str, task_id: int = None, feature_id: int = None):
        self.model = model
        self.mode = mode
        self.task_id = task_id 
        self.feature_id = feature_id 
        self.engine = UnifiedEngine()
        print(f"Agent initialized. Mode: {self.mode}, Model: {self.model}. Running in Safe Mode.")

    def run(self):
        run_count = 0
        while True:
            run_count += 1
            print(f"\n--- Starting Cycle {run_count} ---")
            should_continue = self._execute_cycle()
            if not should_continue or self.mode == 'single':
                break
        print("\n--- Agent has finished all work. ---")

    def _execute_cycle(self) -> bool:
        repo_url = self._get_repo_url()
        git_manager = GitManager(repo_url=repo_url)
        if not git_manager.setup_repository():
            return False
        tools_instance = AgentTools(git_manager.repo_path, git_manager)
        context = self._gather_context(git_manager.repo_path)

        # Build initial conversation messages
        messages = self.engine._build_prompt(context, self.task_id, self.feature_id)

        # Conversational loop to support multi-turn tool usage (Feature 7.15)
        max_turns = 8
        turn = 0
        while True:
            turn += 1
            response_text = self.engine._make_api_call(self.model, messages)
            print("\n--- LLM Response Received ---\n")
            print(response_text)

            # Append assistant's JSON response to the conversation history
            messages.append({"role": "assistant", "content": response_text})

            # Parse the JSON
            try:
                json_str = response_text.strip()
                if json_str.startswith("```json"): json_str = json_str[7:-4].strip()
                data = json.loads(json_str)
            except json.JSONDecodeError as e:
                print(f"Error: Failed to decode LLM response as JSON: {e}", file=sys.stderr)
                return False

            print("\n--- Agent's Plan ---")
            print(data.get("plan", "No plan provided."))

            tool_calls = data.get("tool_calls", [])
            if not tool_calls:
                print("No tool calls returned by the agent. Halting.")
                return False

            results, halt = self._execute_and_collect_tool_calls(tools_instance, tool_calls)

            if halt:
                # ask_question or finish signaled a halt condition
                return False

            # If the agent invoked finish (even without a HALT string), end this cycle
            if any(call.get("tool_name") == "finish" for call in tool_calls):
                return False

            # Provide tool execution results back to the agent for the next turn
            feedback = {
                "type": "tool_results",
                "results": results
            }
            messages.append({
                "role": "user",
                "content": (
                    "Tool execution results:\n" + json.dumps(feedback, indent=2) +
                    "\nContinue by returning your next JSON response following the required schema."
                )
            })

            if turn >= max_turns:
                print("Max conversation turns reached; ending cycle.")
                return True

    def _execute_and_collect_tool_calls(self, tools_instance: AgentTools, tool_calls: list) -> tuple[list, bool]:
        print("\n--- Executing Tool Calls ---")
        results = []
        for call in tool_calls:
            tool_name = call.get("tool_name")
            # Gracefully accept "arguments" (preferred) or "parameters" (fallback).
            arguments = call.get("arguments", call.get("parameters", {}))
            tool_method = getattr(tools_instance, tool_name, None)
            if not tool_method:
                msg = f"Error: Unknown tool implementation '{tool_name}'."
                print(msg)
                results.append({"tool_name": tool_name, "arguments": arguments, "error": msg})
                continue
            print(f"Calling Tool: {tool_name}({arguments})")
            try:
                result = tool_method(**arguments)
                print(f"Tool Result: {result}")
                results.append({"tool_name": tool_name, "arguments": arguments, "result": result})
                # If ask_question or finish indicates HALT, stop the cycle
                if tool_name in ['ask_question', 'finish'] and isinstance(result, str) and "HALT" in result:
                    return results, True
            except Exception as e:
                err = f"Error executing tool '{tool_name}': {e}"
                print(err)
                results.append({"tool_name": tool_name, "arguments": arguments, "error": err})
                return results, True
        return results, False
    
    def _gather_context(self, repo_path: str):
        files = [
            "tasks/TASKS.md",
            "docs/AGENT_PRINCIPLES.md",
            "docs/FEATURE_FORMAT.md",
            "docs/FILE_ORGANISATION.md",
            "docs/LOCAL_SETUP.md",
            "docs/PLAN_SPECIFICATION.md",
            "docs/SPEC.md",
            "docs/SPECIFICATION_GUIDE.md",
            "docs/TASK_FORMAT.md",
            "docs/TOOL_ARCHITECTURE.md",
            "scripts/run_local_agent.py",
            "scripts/git_manager.py",
            "tasks/7/plan_7.md"
        ]

        if self.task_id:
            task_plan_path = f"tasks/{self.task_id}/plan_{self.task_id}.md"
            if task_plan_path not in files:
                files.append(task_plan_path)

        context = {}
        for filename in files:
            try:
                with open(os.path.join(repo_path, filename), "r") as f: context[filename] = f.read()
            except FileNotFoundError: pass
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
    parser.add_argument('--task_id', type=int, help="Specify a task ID to work on.")
    parser.add_argument('--feature_id', type=int, help="Specify a feature ID within the task to work on.")
    args = parser.parse_args()
    
    agent = Agent(model=args.model, mode=args.mode, task_id=args.task_id, feature_id=args.feature_id)
    agent.run()
