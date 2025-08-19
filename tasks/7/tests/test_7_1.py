import os
import sys

def run():
    path = "scripts/run_local_agent.py"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    required = ["class Agent", "class AgentTools"]
    missing = [s for s in required if s not in content]
    if missing:
        print("FAIL: run_local_agent.py missing: " + ", ".join(missing))
        sys.exit(1)
    print("PASS: Task 7 - run_local_agent.py exists and contains Agent classes.")
    sys.exit(0)

if __name__ == "__main__":
    run()
