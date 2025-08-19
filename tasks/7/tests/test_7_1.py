import os, sys

def run():
    path = "scripts/run_local_agent.py"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    required_snippets = ["class Agent", "class AgentTools", "def run(self)"]
    missing = [s for s in required_snippets if s not in content]
    if missing:
        print("FAIL: run_local_agent.py missing: " + ", ".join(missing))
        sys.exit(1)
    print("PASS: Task 7 acceptance verified.")
    sys.exit(0)

if __name__ == "__main__":
    run()
