import os, sys

def run():
    path = "scripts/run_local_agent.py"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if "class Agent" not in content and "class AgentTools" not in content:
        print("FAIL: run_local_agent.py missing Agent or AgentTools class definitions.")
        sys.exit(1)
    print("PASS: Task 7 verified: run_local_agent.py exists and contains agent-related classes.")
    sys.exit(0)

if __name__ == "__main__":
    run()
