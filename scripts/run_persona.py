import argparse
import os
import sys
from dotenv import load_dotenv

# Ensure repository root is on sys.path
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from scripts.run_local_agent import Agent


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="Run a specific agent persona against a task.")
    parser.add_argument('--persona', required=True, choices=['manager', 'planner', 'tester', 'developer'], help='Which persona to run')
    parser.add_argument('--task', required=True, type=int, help='Task ID to target')
    parser.add_argument('--feature', type=int, help='Optional feature number within the task (e.g., 10.3 -> 3)')
    parser.add_argument('--model', type=str, default='ollama/llama3', help='LiteLLM model to use')
    parser.add_argument('--mode', choices=['single', 'continuous'], default='single', help='Execution mode')
    args = parser.parse_args()

    agent = Agent(model=args.model, mode=args.mode, task_id=args.task, feature_id=args.feature, persona=args.persona)
    agent.run()


if __name__ == '__main__':
    main()
