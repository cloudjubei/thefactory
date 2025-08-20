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
from scripts.tools.finish_feature import finish_feature_tool
from scripts.tools.run_tests import run_tests_tool
from scripts.tools.task_utils import get_task, update_feature_status

class AgentTools:\n    def __init__(self, repo_path: str, git_manager: GitManager):
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
        return finish_tool(self.git_manager, reason)

    def finish_feature(self, task_id: int, feature_id: int, title: str, message: str = ""):
        return finish_feature_tool(self.git_manager, task_id, feature_id, title, message)

    def run_tests(self):
        return run_tests_tool(self.repo_path)

    def update_feature_status(self, task_id: int, feature_number: int, new_status: str, reason: str = ""):
        """Expose update_feature_status as an agent tool."""
        # Ensure the function uses the working repo tasks base path
        tasks_base = os.path.join(self.repo_path, 'tasks')
        return update_feature_status(task_id=task_id, feature_number=feature_number, new_status=new_status, reason=reason, base_path=tasks_base)

class UnifiedEngine:
    def _build_prompt(self, context: dict, task_id: int = None, feature_id: int = None, persona: str = None) -> list:
        context_str = "\n".join(f"--- START of {name} ---\n{content}\n--- END of {name} ---\n" for name, content in context.items())

        persona_blocks = {
            "manager": (
                "You are the Manager persona.\n"
                "Objectives: validate and refine the task description; ensure completeness; create or refine a plan only if needed to unblock work.\n"
                "Constraints: do not implement code or tests. Prefer minimal, precise edits and reference specs.\n"
                "Primary tools: retrieve_context_files, write_file, ask_question.\n"
            ),
            "planner": (
                "You are the Planner persona.\n"
                "Objectives: create/update tasks/{task_id}/plan.md following PLAN_SPECIFICATION and FEATURE_FORMAT.\n"
                "Constraints: do not implement code. Keep the plan concise and specification-driven.\n"
                "Primary tools: retrieve_context_files, write_file.\n"
            ),
            "tester": (
                "You are the Tester persona.\n"
                "Objectives: write tests under tasks/{task_id}/tests/ that encode acceptance criteria for features. Use run_tests to validate.\n"
                "Constraints: do not implement features. Tests must be deterministic and specific.\n"
                "Primary tools: retrieve_context_files, write_file, run_tests.\n"
            ),
            "developer": (
                "You are the Developer persona.\n"
                "Objectives: implement exactly ONE pending feature from tasks/{task_id}/plan.md, write tests, run tests, and complete the feature.\n"
                "Constraints: one feature per cycle; minimal incremental changes; strictly follow acceptance criteria.\n"
                "Primary tools: retrieve_context_files, write_file, run_tests, finish_feature.\n"
                "Note: If update_feature_status is unavailable, update the plan file directly using write_file.\n"
            ),
        }

        persona_instructions = ""
        if persona:
            block = persona_blocks.get(persona, "")
            persona_instructions = f"\n\nPersona Mode: {persona}\n{block}\n"

        system_prompt = f"""
You are an autonomous AI agent. Your goal is to advance a software project by completing one task.
You operate by generating a plan and a sequence of tool calls in a single JSON response.

You have access to the following SAFE tools:
- `write_file(path, content)`
- `retrieve_context_files(paths: list)`
- `rename_files(operations: list, overwrite: bool, dry_run: bool)`
- `run_tests()`
- `finish_feature(task_id, feature_id, title, message)`
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
    b.  `submit_for_review` with the correct `task_id` and `task_title`.
    c.  `finish` to end the cycle.

If no tasks are eligible, your ONLY tool call is `finish(reason=\"HALT: No eligible tasks found.\")`.
Respond with a single, valid JSON object.{persona_instructions}
"""
        user_prompt_parts = ["### PROJECT CONTEXT", context_str]

        if task_id:
            specific_task_instruction = f"You are instructed to work on Task {task_id}."
            if feature_id:
                specific_task_instruction += f" Specifically, focus on Feature {task_id}.{feature_id} within this task."
            specific_task_instruction += " Ignore the '1. Analyze the context to identify the next eligible pending task.' step and directly formulate a plan and tool calls for this specific task/feature."
            if persona:
                specific_task_instruction += f" You are running in persona mode: {persona}."
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

class Agent:
    def __init__(self, model: str, mode: str, task_id: int, feature_id: int = None, persona: str = None):
        self.model = model
        self.mode = mode
        self.task_id = task_id
        self.feature_id = feature_id
        self.persona = persona
        self.working_dir = f"/tmp/agent_repo_{self.task_id}"
        self.engine = UnifiedEngine()
        print(f"Agent initialized. Mode: {self.mode}, Model: {self.model}. Persona: {self.persona or 'generic'}. Running in Safe Mode.")

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
        git_manager = GitManager(repo_url=repo_url, working_dir=self.working_dir)
        if not git_manager.setup_repository(branch_name=f"features/{self.task_id}"):
            return False
        tools_instance = AgentTools(git_manager.repo_path, git_manager)
        context = self._gather_context(git_manager.repo_path, self.persona)

        # Build initial conversation messages
        messages = self.engine._build_prompt(context, self.task_id, self.feature_id, self.persona)

        # Conversational loop to support multi-turn tool usage
        max_turns = 8
        for turn in range(max_turns):
            print(f"\n--- Conversation Turn {turn + 1}/{max_turns} ---")
            response_text = self.engine._make_api_call(self.model, messages)
            print("\n--- LLM Response Received ---")
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
                return False  # ask_question or finish signaled a halt

            # If the agent invoked finish (even without HALT), end this cycle
            if any(call.get("tool_name") == "finish" for call in tool_calls):
                return True  # Cycle complete, might start another in continuous mode

            # Provide tool execution results back to the agent for the next turn
            feedback = {"type": "tool_results", "results": results}
            messages.append({
                "role": "user",
                "content": (
                    "Tool execution results:\n" + json.dumps(feedback, indent=2) +
                    "\nContinue by returning your next JSON response following the required schema."
                )
            })

        print("Max conversation turns reached; ending cycle.")
        return True

    def _execute_and_collect_tool_calls(self, tools_instance: AgentTools, tool_calls: list) -> tuple[list, bool]:
        print("\n--- Executing Tool Calls ---")
        results = []
        for call in tool_calls:
            tool_name = call.get("tool_name")
            arguments = call.get("arguments", call.get("parameters", {}))
            tool_method = getattr(tools_instance, tool_name, None)
            if not tool_method:
                msg = f"Error: Unknown tool implementation '{tool_name}'."
                print(msg)
                results.append({"tool_name": tool_name, "arguments": arguments, "error": msg})
                continue
            print(f"Calling Tool: {tool_name}({arguments})")
            try:
                result = tool_method(**arguments) if isinstance(arguments, dict) else tool_method()
                print(f"Tool Result: {result}")
                results.append({"tool_name": tool_name, "arguments": arguments, "result": result})
                if tool_name in ['ask_question', 'finish'] and isinstance(result, str) and "HALT" in result:
                    return results, True
            except Exception as e:
                err = f"Error executing tool '{tool_name}': {e}"
                print(err)
                results.append({"tool_name": tool_name, "arguments": arguments, "error": err})
                return results, True
        return results, False

    def _gather_context(self, repo_path: str, persona: str | None = None):
        files = []

        # Minimal context selection per persona
        if persona == 'manager':
            files = [
                'docs/tasks/TASKS_GUIDANCE.md',
                'docs/AGENT_PRINCIPLES.md',
                'docs/TOOL_ARCHITECTURE.md',
            ]
        elif persona == 'planner':
            files = [
                'docs/PLAN_SPECIFICATION.md',
                'docs/FEATURE_FORMAT.md',
                'docs/tasks/TASKS_GUIDANCE.md',
                'docs/TOOL_ARCHITECTURE.md',
            ]
        elif persona == 'tester':
            files = [
                'docs/TESTING.md',
                'docs/PLAN_SPECIFICATION.md',
                'docs/TOOL_ARCHITECTURE.md',
            ]
        elif persona == 'developer':
            files = [
                'docs/AGENT_EXECUTION_CHECKLIST.md',
                'docs/PLAN_SPECIFICATION.md',
                'docs/TESTING.md',
                'docs/TOOL_ARCHITECTURE.md',
            ]
        else:
            # Generic mode: broader context
            files = [
                'docs/AGENT_EXECUTION_CHECKLIST.md',
                'docs/AGENT_PRINCIPLES.md',
                'docs/FEATURE_FORMAT.md',
                'docs/FILE_ORGANISATION.md',
                'docs/LOCAL_SETUP.md',
                'docs/PLAN_SPECIFICATION.md',
                'docs/SPEC.md',
                'docs/SPECIFICATION_GUIDE.md',
                'docs/tasks/TASKS_GUIDANCE.md',
                'docs/TESTING.md',
                'docs/TOOL_ARCHITECTURE.md',
                'scripts/run_local_agent.py',
            ]

        # Always include the orchestrator file reference for tool contract visibility
        if 'scripts/run_local_agent.py' not in files:
            files.append('scripts/run_local_agent.py')

        context = {}
        # The sole source of truth for tasks is now the task.json file.
        if self.task_id:
            task_data = get_task(self.task_id, base_path=os.path.join(repo_path, 'tasks'))
            if task_data:
                context[f'tasks/{self.task_id}/task.json'] = json.dumps(task_data, indent=2)

        for filename in files:
            if filename in context:
                continue
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
    def _get_working_dir(self):
        return f"/tmp/agent_repo_{self.task_id}"

if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser(description="Autonomous AI Agent for Specification Programming.")
    parser.add_argument('--model', type=str, default='ollama/llama3', help="The LiteLLM model string.")
    parser.add_argument('--mode', choices=['single', 'continuous'], default='single', help="Execution mode.")
    parser.add_argument('--task', required=True, type=int, help="Specify a task ID to work on.")
    parser.add_argument('--feature', type=int, help="Specify a feature ID within the task to work on.")
    parser.add_argument('--persona', choices=['manager', 'planner', 'tester', 'developer'], help='Run in persona mode with tailored prompts and minimal context.')
    args = parser.parse_args()

    agent = Agent(model=args.model, mode=args.mode, task_id=args.task, feature_id=args.feature, persona=args.persona)
    agent.run()
