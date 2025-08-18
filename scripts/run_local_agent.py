import argparse
import json
import os
import sys
from dotenv import load_dotenv

# This script assumes that the tool functions are implemented in
# sibling files as per the project's file organization specification.
# For example, `write_file` is in `scripts/tools/write_file.py`.
# As this task is to create the orchestrator, we will assume these files
# will be created by other tasks. For now, we define placeholders.

# Placeholder for a real LLM client implementation
class LLMClient:
    """A placeholder for a client that interacts with an LLM API."""
    def __init__(self, model):
        self.model = model
        print(f"Initializing LLM client for model: {self.model}")
        # In a real implementation, you would load API keys and set up
        # the client (e.g., OpenAI, Anthropic, LiteLLM).
        if "OPENAI_API_KEY" not in os.environ and "GROQ_API_KEY" not in os.environ and "GEMINI_API_KEY" not in os.environ:
             print("Warning: No major API keys found in environment. The agent may not work as expected with cloud models.")

    def call(self, messages):
        """Makes a call to the LLM and returns the response."""
        # This is where the actual API call to the LLM would happen.
        # The implementation will depend on the chosen provider.
        raise NotImplementedError("LLMClient.call() must be implemented by a specific LLM provider wrapper.")

# Placeholder for tool implementations
class AgentTools:
    """A dispatcher for all available agent tools."""
    def __init__(self):
        # In a real scenario, these would be imported from their respective files.
        self.tools = {
            # "write_file": write_file,
            # "retrieve_context_files": retrieve_context_files,
            # "rename_files": rename_files,
            # "submit_for_review": submit_for_review,
            # "ask_question": ask_question,
            # "finish": finish,
        }
    
    def dispatch(self, tool_name, arguments):
        """Calls the appropriate tool with the given arguments."""
        if tool_name in self.tools:
            return self.tools[tool_name](**arguments)
        raise ValueError(f"Unknown tool: {tool_name}. Available tools: {list(self.tools.keys())}")

def get_system_context():
    """Reads core specification files to provide context to the agent."""
    context_files = [
        "docs/SPEC.md",
        "docs/AGENT_PRINCIPLES.md",
        "docs/FILE_ORGANISATION.md",
        "docs/PLAN_SPECIFICATION.md",
        "docs/FEATURE_FORMAT.md",
        "docs/TASK_FORMAT.md",
        "docs/TOOL_ARCHITECTURE.md",
        "tasks/TASKS.md",
    ]
    
    content = "You are an autonomous AI agent. Your goal is to advance a software project by completing one task.\n"
    content += "Here is the current project context:\n\n"
    
    for file_path in context_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content += f"--- START of {file_path} ---\n"
                content += f.read()
                content += f"\n--- END of {file_path} ---\n\n"
        except FileNotFoundError:
            content += f"Warning: Could not find context file {file_path}.\n"
            
    return content

def construct_initial_prompt(task_id, feature_id=None):
    """Constructs the initial user prompt based on the specified task."""
    prompt = f"Your task is to work on Task {task_id}."
    
    plan_path = f"tasks/{task_id}/plan_{task_id}.md"
    if os.path.exists(plan_path):
        with open(plan_path, 'r', encoding='utf-8') as f:
            plan_content = f.read()
        prompt += f"\nA plan for this task already exists:\n\n--- START of {plan_path} ---\n{plan_content}\n--- END of {plan_path} ---\n"
    else:
        prompt += " No plan exists for this task yet. You must create one."

    if feature_id:
        prompt += f"\nYou should focus specifically on feature {feature_id} from the plan."
    
    prompt += "\n\nGenerate a JSON response with your plan and the first set of tool calls to begin working on the task."
    return prompt
    
def main():
    """The main entry point for the agent orchestrator."""
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="Run the AI agent orchestrator.")
    parser.add_argument("--model", type=str, default="ollama/llama3", help="The LLM model to use (e.g., 'gpt-4o', 'groq/llama3-70b-8192').")
    parser.add_argument("--mode", type=str, choices=["single", "continuous"], default="single", help="Execution mode.")
    parser.add_argument("--task", type=int, required=True, help="The ID of the task to work on.")
    parser.add_argument("--feature", type=str, help="The ID of the specific feature to work on (e.g., '7.8').")
    
    args = parser.parse_args()

    print(f"Starting agent with model: {args.model}, mode: {args.mode}, task: {args.task}")

    try:
        llm_client = LLMClient(args.model)
        tools = AgentTools()
    except Exception as e:
        print(f"Error during initialization: {e}")
        sys.exit(1)

    system_prompt = get_system_context()
    user_prompt = construct_initial_prompt(args.task, args.feature)
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    # Main conversational loop
    while True:
        try:
            raw_response = llm_client.call(messages)
        except NotImplementedError:
            print("FATAL: The LLMClient is a placeholder and not implemented. Cannot proceed.")
            break
        except Exception as e:
            print(f"Error calling LLM: {e}")
            break
        
        try:
            response_data = json.loads(raw_response)
            plan = response_data.get("plan", "No plan provided.")
            tool_calls = response_data.get("tool_calls", [])
            print(f"\nAgent Plan: {plan}\n")
        except json.JSONDecodeError:
            print(f"Error: Failed to decode LLM response into JSON.\nResponse:\n{raw_response}")
            break

        if not tool_calls:
            print("Agent provided no tool calls. Ending cycle.")
            break

        tool_outputs = []
        should_terminate = False
        
        for call in tool_calls:
            tool_name = call.get("tool_name")
            arguments = call.get("arguments", {})
            
            try:
                output = tools.dispatch(tool_name, arguments)
                tool_outputs.append({"tool_name": tool_name, "output": json.dumps(output)})
                
                if tool_name in ["finish", "ask_question", "submit_for_review"]:
                    should_terminate = True
            except Exception as e:
                error_message = f"Error executing tool {tool_name}: {e}"
                print(error_message)
                tool_outputs.append({"tool_name": tool_name, "output": json.dumps({"ok": False, "error": error_message})})
        
        if should_terminate:
            print("Terminating tool called. Ending cycle.")
            break
            
        messages.append({"role": "assistant", "content": raw_response})
        messages.append({"role": "user", "content": f"tool_outputs: {json.dumps(tool_outputs)}"})

        if args.mode == "single":
            print("Single mode: exiting after one iteration.")
            break

if __name__ == "__main__":
    main()
