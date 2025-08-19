import os
import sys

def run():
    path = os.path.join("scripts", "run_local_agent.py")
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    markers = ["class Agent", "class AgentTools", "UnifiedEngine"]
    if not any(m in content for m in markers):
        print("FAIL: run_local_agent.py does not appear to define the orchestrator classes.")
        sys.exit(1)

    print("PASS: Orchestrator script exists and contains orchestrator classes.")
    sys.exit(0)

if __name__ == "__main__":
    run()
