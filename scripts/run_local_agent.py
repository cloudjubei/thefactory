import argparse
import json
import os
import sys
from dotenv import load_dotenv
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable

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

# --- Tool Mapping ---

def get_available_tools(agent_type: str, git_manager: GitManager) -> Dict[str, Callable]:
    """Returns a dictionary of callable tool functions based on the agent persona."""
    base_tools = {
        "finish": task_utils.finish,
        "update_agent_question": task_utils.update_agent_question,
    }

    agent_tools = {}
    if agent_type == 'developer':
        agent_tools = {
            "get_context": task_utils.get_context,
            "write_file": task_utils.write_file,
            "run_test": task_utils.run_test,
            "update_feature_status": task_utils.update_feature_status,
            "defer_feature": task_utils.defer_feature,
            "finish_feature": lambda **kwargs: task_utils.finish_feature(**kwargs, git_manager=git_manager),
        }
    elif agent_type == 'planner':
        agent_tools = {
            "update_feature_plan": task_utils.update_feature_plan,
            "create_feature": task_utils.create_feature,
        }
    elif agent_type == 'tester':
        agent_tools = {
            "update_acceptance_criteria": task_utils.update_acceptance_criteria,
            "update_test": task_utils.update_test,
            "run_test": task_utils.run_test,
            "get_test": task_utils.get_test,
            "delete_test": task_utils.delete_test,
        }
    
    base_tools.update(agent_tools)
    return base_tools

def construct_system_prompt(agent_type: str, task: Task, feature: Feature, context: str, available_tools: Dict) -> str:
    """Constructs the detailed system prompt, now specialized for the agent type."""
    
    # Base information for all agents
    prompt = f"""You are the '{agent_type}' agent.

CURRENT TASK: {task['title']} (ID: {task['id']})
ASSIGNED FEATURE: {feature['title']} (ID: {feature['id']})
DESCRIPTION: {feature.get('description', 'No description specified.')}
"""
    # Acceptance criteria are relevant for developers and testers, but not planners who might be creating them.
    if agent_type in ['developer', 'tester']:
        prompt += "ACCEPTANCE CRITERIA:\n"
        for i, criterion in enumerate(feature.get('acceptance', []), 1):
            prompt += f"{i}. {criterion}\n"

    # --- Agent-specific instructions ---
    if agent_type == 'planner':
        prompt += """
Your **ONLY** job is to create a detailed, step-by-step implementation plan for the assigned feature.
Analyze the feature and use the `update_feature_plan` tool to save your plan. Do not perform any other actions.
"""
    elif agent_type == 'tester':
        prompt += """
Your job is to write the acceptance criteria and a corresponding Python test for this feature.
1. First, use the `update_acceptance_criteria` tool to define the success conditions.
2. Second, use the `update_test` tool to write a test that verifies those criteria.
"""
    else: # Developer prompt
        prompt += f"""
The following context files have been provided:
{context}

Your job is to execute the feature's plan and meet all acceptance criteria.
When you are finished and the tests pass, you MUST call 'finish_feature'.
"""

    prompt += f"""
You must respond in JSON format with a "plan" and a list of "tool_calls".

AVAILABLE TOOLS:
{json.dumps(list(available_tools.keys()), indent=2)}

Begin now.
"""
    return prompt

def run_agent_on_feature(model: str, agent_type: str, task: Task, feature: Feature, git_manager: GitManager):
    print(f"\n--- Activating Agent for Feature: [{feature['id']}] {feature['title']} ---")
    
    available_tools = get_available_tools(agent_type, git_manager)
    context = task_utils.get_context(feature.get("context", []))
    system_prompt = construct_system_prompt(agent_type, task, feature, context, available_tools)

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
            plan = response_json.get("action_plan", "No plan provided.")
            tool_calls = response_json.get("tool_calls", [])
            print(f"Agent Plan: {plan}")

            if not tool_calls: continue

            tool_outputs = []
            for call in tool_calls:
                tool_name = call.get("tool_name")
                tool_args = call.get("arguments", {})
                
                print(f"Executing Tool: {tool_name} with args: {tool_args}")
                
                if tool_name in available_tools:
                    tool_args.setdefault('task_id', task['id'])
                    tool_args.setdefault('feature_id', feature['id'])
                    result = available_tools[tool_name](**tool_args)
                    tool_outputs.append(f"Tool {tool_name} returned: {result}")
                else:
                    tool_outputs.append(f"Error: Tool '{tool_name}' not found.")

                if tool_name in ['finish_feature', 'defer_feature']:
                    print(f"Agent called '{tool_name}'. Concluding work on this feature.")
                    return True
                if tool_name == 'finish':
                    print("Agent called 'finish'. Terminating orchestrator.")
                    return False

            messages.append({"role": "user", "content": "--- TOOL RESULTS ---\n" + "\n".join(tool_outputs)})

        except Exception as e:
            print(f"An error occurred in agent loop: {e}")
            task_utils.defer_feature(task['id'], feature['id'], f"Agent loop failed: {e}")
            return True
            
    print(f"Max turns reached for feature {feature['id']}. Deferring.")
    task_utils.defer_feature(task['id'], feature['id'], "Max conversation turns reached.")
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
    
    while True:
        current_task = task_utils.get_task(current_task['id'])
        next_feature = task_utils.find_next_available_feature(current_task)
        
        if not next_feature:
            print(f"\nNo more available features for task {current_task['id']}.")
            break
            
        should_continue = run_agent_on_feature(model, agent_type, current_task, next_feature, git_manager)
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