import argparse
import json
import os
import sys
from dotenv import load_dotenv
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable, Tuple

# Add project root to sys.path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from litellm import completion
from docs.tasks.task_format import Task, Feature
from scripts.git_manager import GitManager
import scripts.task_utils as task_utils

load_dotenv()

# --- Constants ---
MAX_TURNS_PER_FEATURE = 10
PROJECT_ROOT = Path(__file__).resolve().parent.parent

try:
    PROTOCOL_EXAMPLE_PATH = PROJECT_ROOT / "docs" / "agent_response_example.json"
    with open(PROTOCOL_EXAMPLE_PATH, "r") as f:
        # Load and then dump with indentation to create a nicely formatted string for the prompt
        PROTOCOL_EXAMPLE_STR = json.dumps(json.load(f), indent=2)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"FATAL: Could not load or parse agent_response_example.json: {e}")
    # Provide a safe fallback if the file is missing or corrupt
    PROTOCOL_EXAMPLE_STR = '{\n  "thoughts": "Your reasoning here...",\n  "tool_calls": [ ... ]\n}'

# --- Tool Mapping ---

def get_available_tools(agent_type: str, git_manager: GitManager) -> Tuple[Dict[str, Callable], List[str]]:
    """
    Returns a tuple containing:
    1. A dictionary of callable tool functions.
    2. A list of formatted tool signature strings for the prompt.
    """
    base_tools = {
        "get_context": (task_utils.get_context, "get_context(files: list[str]) -> list[str]"),
        "block_feature": (task_utils.block_feature, "block_feature(reason: str)"),
        "finish_feature": (
            lambda **kwargs: task_utils.finish_feature(**kwargs, agent_type=agent_type, git_manager=git_manager),
            "finish_feature()"
        ),
    }

    agent_tools = {}
    # The signatures are simplified for the agent. The orchestrator handles the rest.
    if agent_type == 'developer':
        agent_tools = {
            "write_file": (task_utils.write_file, "write_file(filename: str, content: str)"),
            "run_test": (task_utils.run_test, "run_test() -> str"),
        }
    elif agent_type == 'planner':
        agent_tools = {
            "update_feature_plan": (task_utils.update_feature_plan, "update_feature_plan(plan: str)"),
            "create_feature": (task_utils.create_feature, "create_feature(feature: dict)"),
        }
    elif agent_type == 'tester':
        agent_tools = {
            "update_acceptance_criteria": (task_utils.update_acceptance_criteria, "update_acceptance_criteria(criteria: list[str])"),
            "update_test": (task_utils.update_test, "update_test(test: str)"),
            "run_test": (task_utils.run_test, "run_test() -> str")
        }
    
    base_tools.update(agent_tools)
    
    # Unzip the dictionary into two separate structures
    tool_functions = {name: func for name, (func, sig) in base_tools.items()}
    tool_signatures = [sig for name, (func, sig) in base_tools.items()]
    
    return tool_functions, tool_signatures

def construct_system_prompt(agent_type: str, task: Task, feature: Feature, context: str, tool_signatures: List[str]) -> str:
    """Constructs the detailed system prompt, specialized for the agent type."""
    prompt = f"""You are the '{agent_type}' agent.
CURRENT TASK: {task['title']} (ID: {task['id']})
ASSIGNED FEATURE: {feature['title']} (ID: {feature['id']})
DESCRIPTION: {feature.get('description', 'No description specified.')}
"""
    if agent_type in ['developer', 'tester']:
        prompt += "ACCEPTANCE CRITERIA:\n"
        for i, criterion in enumerate(feature.get('acceptance', []), 1):
            prompt += f"{i}. {criterion}\n"

    # --- Agent-specific instructions ---
    if agent_type == 'planner':
        prompt += """
Your **ONLY** job is to create a detailed, step-by-step implementation plan for the assigned feature.
Analyze the feature and use the `update_feature_plan` tool to save your plan.
When you are done, you **MUST** call `finish_feature` to mark it as ready for the next stage.
"""
    elif agent_type == 'tester':
        prompt += """
Your job is to write the acceptance criteria and a corresponding Python test for this feature.
1. First, use the `update_acceptance_criteria` tool to define the success conditions.
2. Second, use the `update_test` tool to write a test that verifies those criteria.
When you are done, you **MUST** call `finish_feature` to mark it as ready for development.
"""
    else: # Developer prompt
        prompt += f"""
The following context files have been provided:
{context}
Your job is to execute the feature's plan and meet all acceptance criteria.
When you are finished and the tests pass, you **MUST** call `finish_feature`.
"""

    prompt += f"""
You **MUST** respond in a single, valid JSON object. This object must adhere to the following structure:
```json
{PROTOCOL_EXAMPLE_STR}
```
The thoughts field is for your reasoning, and tool_calls is a list of actions to execute.
Your response will be parsed as JSON. Do not include any text outside of this JSON object.
"""
    prompt += """
Your available tools are defined below. Call them with the exact function and argument names.
--- TOOL SIGNATURES ---
"""
    for sig in tool_signatures:
        prompt += f"- {sig}\n"
        prompt += "--- END OF TOOL SIGNATURES ---\n"
        
    prompt += "\nBegin now."
    return prompt

def run_agent_on_feature(model: str, agent_type: str, task: Task, feature: Feature, git_manager: GitManager):
    print(f"\n--- Activating Agent for Feature: [{feature['id']}] {feature['title']} ---")

    if agent_type == 'developer':
        task_utils.update_feature_status(task['id'], feature['id'], '~')

    available_tools, tool_signatures = get_available_tools(agent_type, git_manager)
    context = task_utils.get_context(feature.get("context", []))
    system_prompt = construct_system_prompt(agent_type, task, feature, context, tool_signatures)

    messages = [{"role": "user", "content": system_prompt}]
    
    if agent_type == 'developer':
        task_utils.update_feature_status(task['id'], feature['id'], '~')

    for i in range(MAX_TURNS_PER_FEATURE):
        print(f"\n--- Feature Turn {i+1}/{MAX_TURNS_PER_FEATURE} ---")
        
        try:
            response = completion(model=model, messages=messages, response_format={"type": "json_object"})
            assistant_message = response.choices[0].message
            messages.append(assistant_message)
            
            response_json = json.loads(assistant_message.content)
            thoughts = response_json.get("thoughts", "No thoughts provided.")
            tool_calls = response_json.get("tool_calls", [])
            print(f"Agent Thoughts: {thoughts}")

            if not tool_calls: continue

            tool_outputs = []
            for call in tool_calls:
                tool_name = call.get("tool_name", call.get("tool", call.get("name", "unknown_tool")))
                tool_args = call.get("arguments", call.get("parameters", {}))
                
                print(f"Executing Tool: {tool_name} with args: {tool_args}")
                
                if tool_name in available_tools:
                    tool_args.setdefault('task_id', task['id'])
                    tool_args.setdefault('feature_id', feature['id'])
                    result = available_tools[tool_name](**tool_args)
                    tool_outputs.append(f"Tool {tool_name} returned: {result}")
                else:
                    tool_outputs.append(f"Error: Tool '{tool_name}' not found.")

                if tool_name in ['finish_feature', 'block_feature']:
                    print(f"Agent called '{tool_name}'. Concluding work on this feature.")
                    return True
                if tool_name == 'finish':
                    print("Agent called 'finish'. Terminating orchestrator.")
                    return False

            messages.append({"role": "user", "content": "--- TOOL RESULTS ---\n" + "\n".join(tool_outputs)})

        except Exception as e:
            print(f"An error occurred in agent loop: {e}")
            task_utils.block_feature(task['id'], feature['id'], f"Agent loop failed: {e}")
            return True
            
    print(f"Max turns reached for feature {feature['id']}. Deferring.")
    task_utils.block_feature(task['id'], feature['id'], "Max conversation turns reached.")
    return True


def run_orchestrator(model: str, agent_type: str, task_id: Optional[int]):
    print("--- Starting Autonomous Orchestrator ---")
    
    if task_id:
        current_task = task_utils.get_task(task_id)
    else:
        current_task = task_utils.find_next_pending_task()

    if not current_task:
        print("No available tasks to work on.")
        return

    print(f"Selected Task: [{current_task['id']}] {current_task['title']}")
    git_manager = GitManager()
    
    processed_feature_ids = set()
    while True:
        current_task = task_utils.get_task(current_task['id'])
        
        next_feature = task_utils.find_next_available_feature(current_task, exclude_ids=processed_feature_ids)
        if not next_feature:
            print(f"\nNo more available features for task {current_task['id']}.")
            break
            
        should_continue = run_agent_on_feature(model, agent_type, current_task, next_feature, git_manager)
        processed_feature_ids.add(next_feature['id'])
        if not should_continue:
            break
    print("\n--- Orchestrator Finished ---")

def main():
    parser = argparse.ArgumentParser(description="Run an autonomous AI agent.")
    parser.add_argument("--model", type=str, default="gpt-4-turbo-preview", help="LLM model name.")
    parser.add_argument("--agent", type=str, required=True, choices=['developer', 'tester', 'planner'], help="Agent persona.")
    parser.add_argument("--task", type=int, help="Optional: Specify a task ID to work on.")
    
    args = parser.parse_args()
        
    run_orchestrator(model=args.model, agent_type=args.agent, task_id=args.task)

if __name__ == "__main__":
    main()