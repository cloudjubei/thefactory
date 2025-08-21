import argparse
import json
import os
import sys
from dotenv import load_dotenv
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable

# Add project root to sys.path to allow absolute imports
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from litellm import completion, ModelResponse

from docs.tasks.task_format import Task, Feature
from scripts.git_manager import GitManager
import scripts.task_utils as task_utils

# Load environment variables from .env file
load_dotenv()

# --- Constants ---
MAX_TURNS = 10  # Safety break to prevent infinite loops

# --- Helper Functions ---

def find_next_pending_feature(task: Task) -> Optional[Feature]:
    """Finds the first feature with status '-' in the task."""
    for feature in task.get("features", []):
        if feature.get("status") == "-":
            return feature
    return None

def gather_context(feature: Feature) -> str:
    """
    Gathers the content of all files listed in the feature's context
    and formats it into a single string.
    """
    context_str = "--- START OF CONTEXT FILES ---\n\n"
    for file_path_str in feature.get("context", []):
        file_path = Path(file_path_str)
        context_str += f"--- FILE: {file_path_str} ---\n"
        try:
            content = file_path.read_text()
            context_str += f"{content}\n"
        except FileNotFoundError:
            context_str += f"File not found at path: {file_path_str}\n"
        except Exception as e:
            context_str += f"Error reading file {file_path_str}: {e}\n"
        context_str += f"--- END OF FILE: {file_path_str} ---\n\n"
    context_str += "--- END OF CONTEXT FILES ---\n"
    return context_str

def get_available_tools(agent_type: str, git_manager: GitManager) -> Dict[str, Callable]:
    """
    Returns a dictionary mapping tool names to their callable function
    implementations for the given agent type.
    """
    # Base tools available to all agents
    all_tools = {
        "update_task_status": task_utils.update_task_status,
        "update_feature_status": task_utils.update_feature_status,
        "update_agent_question": task_utils.update_agent_question,
    }
    
    # Developer-specific tools
    if agent_type == 'developer':
        all_tools.update({
            "get_context": task_utils.get_context,
            "write_file": task_utils.write_file,
            "run_test": task_utils.run_test,
            # Bind the git_manager instance to the finish_feature function
            "finish_feature": lambda **kwargs: task_utils.finish_feature(**kwargs, git_manager=git_manager),
        })

    # Tester-specific tools
    elif agent_type == 'tester':
        all_tools.update({
            "update_acceptance_criteria": task_utils.update_acceptance_criteria,
            "update_test": task_utils.update_test,
            "run_test": task_utils.run_test,
        })
        
    # Planner-specific tools (already covered by the base set)
    elif agent_type == 'planner':
        pass

    return all_tools

def construct_system_prompt(agent_type: str, task: Task, feature: Feature, context: str, available_tools: Dict) -> str:
    """Constructs the detailed system prompt for the LLM."""
    
    prompt = f"""You are the '{agent_type}' agent. Your goal is to complete the assigned feature.
    
    CURRENT TASK: {task['title']} (ID: {task['id']})
    
    CURRENT FEATURE: {feature['title']} (ID: {feature['id']})
    DESCRIPTION: {feature.get('action', 'No action specified.')}
    ACCEPTANCE CRITERIA:
    """
    for i, criterion in enumerate(feature.get('acceptance', []), 1):
        prompt += f"{i}. {criterion}\n"
        
    prompt += f"""
    The following context files have been provided:
    {context}
    
    You must respond in a specific JSON format. Your response must be a single JSON object containing two keys: "plan" and "tool_calls".
    - "plan": A short, high-level, human-readable description of your intended actions for this turn.
    - "tool_calls": An ordered list of tool invocations.
    
    Each tool call in the list must be an object with two keys:
    - "tool_name": The exact name of the tool to call.
    - "arguments": An object containing the parameters for the tool.
    
    AVAILABLE TOOLS:
    {json.dumps(list(available_tools.keys()), indent=2)}
    
    Example Response:
    {{
      "plan": "First, I will update the feature status to 'In Progress', then I will write the required content to the file.",
      "tool_calls": [
        {{
          "tool_name": "update_feature_status",
          "arguments": {{ "task_id": {task['id']}, "feature_id": "{feature['id']}", "status": "~" }}
        }},
        {{
          "tool_name": "write_file",
          "arguments": {{ "filename": "path/to/file.py", "content": "print('Hello, world!')" }}
        }}
      ]
    }}
    
    Begin the work now. Analyze the context and the acceptance criteria, form a plan, and select the appropriate tools to execute it.
    """
    return prompt

# --- Main Orchestrator Logic ---

def run_orchestrator(model: str, agent_type: str, task_id: int, mode: str, feature_id: Optional[str] = None):
    """The main orchestration loop for running the agent."""
    
    print(f"--- Starting Orchestrator ---")
    print(f"Mode: {mode}, Agent: {agent_type}, Task: {task_id}")
    
    try:
        task = task_utils.get_task(task_id)
    except FileNotFoundError:
        print(f"Error: Task with ID {task_id} not found.")
        return

    if feature_id:
        feature = next((f for f in task["features"] if f["id"] == feature_id), None)
        if not feature:
            print(f"Error: Feature with ID {feature_id} not found in task {task_id}.")
            return
    else:
        feature = find_next_pending_feature(task)
        if not feature:
            print("No pending features found in this task. Nothing to do.")
            return

    print(f"Identified feature to work on: [{feature['id']}] {feature['title']}")

    # Initialize tools
    git_manager = GitManager()
    available_tools = get_available_tools(agent_type, git_manager)

    # Prepare for conversation
    context = gather_context(feature)
    system_prompt = construct_system_prompt(agent_type, task, feature, context, available_tools)
    messages = [{"role": "system", "content": system_prompt}]

    for i in range(MAX_TURNS):
        print(f"\n--- Turn {i+1}/{MAX_TURNS} ---")
        
        try:
            response: ModelResponse = completion(
                model=model,
                messages=messages,
                response_format={"type": "json_object"},
            )
            
            assistant_message = response.choices[0].message
            messages.append(assistant_message) # Add LLM response to history
            
            response_json = json.loads(assistant_message.content)
            
            plan = response_json.get("plan", "No plan provided.")
            tool_calls = response_json.get("tool_calls", [])
            
            print(f"Agent Plan: {plan}")
            
            if not tool_calls:
                print("Agent did not request any tool calls. Ending turn.")
                continue

            tool_outputs = []
            should_terminate = False

            for call in tool_calls:
                tool_name = call.get("tool_name")
                tool_args = call.get("arguments", {})
                
                print(f"Executing Tool: {tool_name} with args: {tool_args}")
                
                if tool_name in available_tools:
                    try:
                        # Add task_id and feature_id if they are missing but relevant
                        if 'task_id' not in tool_args:
                            tool_args['task_id'] = task_id
                        if 'feature_id' not in tool_args:
                             tool_args['feature_id'] = feature['id']

                        result = available_tools[tool_name](**tool_args)
                        output = f"Tool {tool_name} executed successfully. Result:\n{result}"
                        tool_outputs.append(output)
                    except Exception as e:
                        output = f"Error executing tool {tool_name}: {e}"
                        print(output)
                        tool_outputs.append(output)
                else:
                    output = f"Error: Tool '{tool_name}' is not available."
                    print(output)
                    tool_outputs.append(output)
                
                # Check for termination conditions
                if (mode == 'single' and tool_name == 'finish_feature') or tool_name == 'finish':
                    should_terminate = True
            
            # Send tool results back to the agent
            tool_results_message = {
                "role": "user",
                "content": "--- TOOL EXECUTION RESULTS ---\n" + "\n---\n".join(tool_outputs)
            }
            messages.append(tool_results_message)
            
            if should_terminate:
                print(f"Termination condition met ('{tool_name}'). Finishing work.")
                break

        except json.JSONDecodeError:
            print("Error: LLM did not return valid JSON. Aborting.")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break
    else:
        print("Maximum number of turns reached. Ending conversation.")

def main():
    """Parses CLI arguments and starts the orchestrator."""
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("ANTHROPIC_API_KEY") and not os.getenv("GOOGLE_API_KEY"):
        print("ERROR: No API key found. Please set OPENAI_API_KEY, ANTHROPIC_API_KEY, or another supported key in your .env file.")
        return

    parser = argparse.ArgumentParser(description="Run a local LLM agent to work on software development tasks.")
    parser.add_argument("--model", type=str, default="gpt-4-turbo-preview", help="The model name to use (e.g., 'openai/gpt-4-turbo').")
    parser.add_argument("--agent", type=str, required=True, choices=['planner', 'tester', 'developer'], help="The type of agent persona to use.")
    parser.add_argument("--task", type=int, required=True, help="The ID of the task to work on.")
    parser.add_argument("--feature", type=str, help="The specific ID of the feature to work on. If omitted, the next pending feature will be selected.")
    parser.add_argument("--mode", type=str, default='single', choices=['single', 'continuous'], help="Execution mode: 'single' for one feature, 'continuous' for the whole task.")
    
    args = parser.parse_args()

    # The user's example used '--persona', which maps directly to '--agent' here.
    run_orchestrator(model=args.model, agent_type=args.agent, task_id=args.task, mode=args.mode, feature_id=args.feature)

if __name__ == "__main__":
    main()