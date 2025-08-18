# scripts/run_local_agent.py
import argparse
import json
import os
import sys
import glob
from datetime import datetime

# --- DUMMY PLACEHOLDERS (as per completed features in plan_7.md) ---

class LlmClient:
    """
    Dummy LLM client placeholder. In a real implementation, this would
    interact with Ollama, OpenAI, Groq, etc.
    """
    def __init__(self, model):
        self.model = model
        print(f"Initializing LLM client for model: {self.model}")

    def get_response(self, messages):
        print("\n--- Sending to LLM ---")
        for msg in messages:
            print(f"[{msg['role']}]")
            # print(f"{msg['content']}") # Content can be very long
        print("----------------------")

        # This is where the actual LLM call would be made.
        # For this dummy version, we'll simulate a multi-step agent response.
        # 1. First, it asks for a file.
        # 2. Then, it writes a file and finishes.
        if len(messages) == 1: # First turn
            print("LLM Simulation: Agent is asking for a file.")
            return {
                "plan": "1. Retrieve `docs/SPEC.md` to understand the project.\n2. Create a new file summarizing the spec.\n3. Finish.",
                "tool_calls": [
                    {
                        "tool_name": "retrieve_context_files",
                        "arguments": {"paths": ["docs/SPEC.md"]}
                    }
                ]
            }
        else: # Second turn
            print("LLM Simulation: Agent is writing a file and finishing.")
            return {
                "plan": "1. Retrieve `docs/SPEC.md` to understand the project.\n2. Create a new file summarizing the spec.\n3. Finish.",
                "tool_calls": [
                    {
                        "tool_name": "write_file",
                        "arguments": {
                            "path": "spec_summary.md",
                            "content": "# Spec Summary\nThis is a summary of the project spec."
                        }
                    },
                    {
                        "tool_name": "submit_for_review",
                        "arguments": {"task_id": 7, "task_title": "Agent Orchestrator"}
                    },
                    {
                        "tool_name": "finish",
                        "arguments": {"reason": "Task completed successfully."}
                    }
                ]
            }

class AgentTools:
    """
    Container for all tools available to the agent.
    Based on features 7.9 - 7.14.
    """
    def write_file(self, path, content):
        print(f"TOOL: write_file(path='{path}')")
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w') as f:
                f.write(content)
            return {"status": "success", "path": path}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def retrieve_context_files(self, paths):
        print(f"TOOL: retrieve_context_files(paths={paths})")
        files = []
        for path in paths:
            try:
                with open(path, 'r') as f:
                    content = f.read()
                files.append({"path": path, "content": content})
            except Exception as e:
                files.append({"path": path, "error": str(e)})
        return {"ok": True, "files": files}

    def rename_files(self, operations):
        print(f"TOOL: rename_files(operations={operations})")
        # Dummy implementation
        return {"status": "success", "summary": f"{len(operations)} files renamed (simulation)."}

    def submit_for_review(self, task_id, task_title):
        print(f"TOOL: submit_for_review(task_id={task_id}, task_title='{task_title}')")
        # Dummy implementation
        return {"status": "success", "pull_request_url": "https://github.com/example/repo/pull/123"}

    def ask_question(self, question_text):
        print(f"TOOL: ask_question(question_text='{question_text}')")
        return {"status": "pending_human_input", "question": question_text}

    def finish(self, reason):
        print(f"TOOL: finish(reason='{reason}')")
        return {"status": "finished", "reason": reason}

# --- Orchestrator Implementation ---

class Orchestrator:
    def __init__(self, model, mode):
        self.mode = mode
        self.llm_client = LlmClient(model)
        self.agent_tools = AgentTools()
        self.messages = []
        self.project_root = os.getcwd()

    def get_context_files_content(self):
        """Reads all core documentation and task files."""
        print("Reading context files...")
        context = []
        # Docs
        for path in glob.glob("docs/*.md"):
            with open(path, 'r') as f:
                context.append(f"--- START of {path} ---\n{f.read()}\n--- END of {path} ---")
        # Tasks
        tasks_path = "tasks/TASKS.md"
        if os.path.exists(tasks_path):
             with open(tasks_path, 'r') as f:
                context.append(f"--- START of {tasks_path} ---\n{f.read()}\n--- END of {tasks_path} ---")
        return "\n\n".join(context)

    def build_system_prompt(self):
        """Constructs the initial system prompt for the agent."""
        context = self.get_context_files_content()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        prompt = f"""
You are an autonomous AI agent. Your goal is to advance a software project by completing one task.
You operate by generating a plan and a sequence of tool calls in a single JSON response.
It is currently {timestamp}.

PROJECT CONTEXT:
{context}

You have access to the following SAFE tools:
- `write_file(path, content)`
- `retrieve_context_files(paths: list)`
- `rename_files(operations: list, overwrite: bool, dry_run: bool)`
- `submit_for_review(task_id, task_title)`
- `ask_question(question_text)`
- `finish(reason)`

YOUR JSON RESPONSE MUST follow this schema precisely:
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

YOUR WORKFLOW IS MANDATORY:
1.  Analyze the context to identify the next eligible pending task.
2.  You can request more context using `retrieve_context_files` tool.
3.  Once you have enough context, formulate a plan to complete the task.
4.  Generate `tool_calls` to:
    a.  `write_file` for all necessary changes.
    b.  `write_file` to update the task's status in `TASKS.md`.
    c.  `submit_for_review` with the correct `task_id` and `task_title`.
    d.  `finish` to end the cycle.

If no tasks are eligible, your ONLY tool call is `finish(reason="HALT: No eligible tasks found.")`.
Respond with a single, valid JSON object. Do not generate any comments or extra text.
        """
        self.messages = [{"role": "system", "content": prompt}]

    def run(self):
        """Main orchestration loop for a single task."""
        print("Starting orchestrator...")
        self.build_system_prompt()
        self.messages.append({"role": "user", "content": "Proceed with the next eligible task."})

        while True:
            response_json = self.llm_client.get_response(self.messages)
            
            # The agent's response should also be part of the history
            self.messages.append({"role": "assistant", "content": json.dumps(response_json, indent=2)})

            tool_calls = response_json.get("tool_calls", [])
            if not tool_calls:
                print("Agent provided no tool calls. Ending run.")
                break

            tool_results, should_terminate = self.execute_tool_calls(tool_calls)

            if should_terminate:
                print("Termination signal received. Ending run.")
                break
            
            # Append tool results for the next turn
            self.messages.append({"role": "user", "content": f"Tool results:\n{json.dumps(tool_results, indent=2)}"})

        print("Orchestrator run finished.")


    def execute_tool_calls(self, tool_calls):
        """Executes tool calls and checks for termination signals."""
        tool_results = []
        should_terminate = False
        
        for call in tool_calls:
            tool_name = call.get("tool_name")
            arguments = call.get("arguments", {})
            
            if hasattr(self.agent_tools, tool_name):
                try:
                    tool_method = getattr(self.agent_tools, tool_name)
                    result = tool_method(**arguments)
                    tool_results.append({"tool_name": tool_name, "result": result})

                    if tool_name in ["finish", "ask_question"]:
                        should_terminate = True

                except Exception as e:
                    tool_results.append({"tool_name": tool_name, "error": f"Error calling tool: {e}"})
            else:
                tool_results.append({"tool_name": tool_name, "error": "Tool not found."})
        
        return tool_results, should_terminate


def main():
    parser = argparse.ArgumentParser(description="Autonomous AI Agent Orchestrator")
    parser.add_argument("--model", type=str, default="ollama/llama3", help="The model to use for the agent.")
    parser.add_argument("--mode", type=str, choices=['single', 'continuous'], default='single', help="Execution mode.")
    args = parser.parse_args()

    orchestrator = Orchestrator(model=args.model, mode=args.mode)
    
    if args.mode == 'continuous':
        print("Continuous mode is enabled. The agent will loop indefinitely.")
        # In a real implementation, this would be a proper loop that re-clones
        # the repo and starts a new Orchestrator instance.
        while True:
            orchestrator.run()
            print("\n--- CYCLE COMPLETE ---")
            print("Restarting for next task in 5 seconds...")
            # time.sleep(5)
            # Re-initialize for the next run
            orchestrator = Orchestrator(model=args.model, mode=args.mode)
    else:
        orchestrator.run()


if __name__ == "__main__":
    main()
