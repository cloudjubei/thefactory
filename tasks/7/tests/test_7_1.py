import os, sys

def run():
    path = "scripts/run_local_agent.py"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()
    required = ["class Agent", "class UnifiedEngine", "class AgentTools"]
    missing = [x for x in required if x not in c]
    if missing:
        print("FAIL: run_local_agent.py missing: " + ", ".join(missing))
        sys.exit(1)
    print("PASS: run_local_agent.py exists with expected classes.")
    sys.exit(0)

if __name__ == "__main__":
    run()
