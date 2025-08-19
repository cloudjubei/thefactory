import os, sys

def run():
    path = "scripts/run_local_agent.py"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    # Check for core classes/identifiers that indicate the orchestrator exists and exposes tools
    required = [
        "class Agent(",
        "class AgentTools(",
        "class UnifiedEngine(",
        "def write_file(",
        "def retrieve_context_files(",
        "def submit_for_review(",
        "def finish_feature(",
        "def run(self)"
    ]
    missing = [s for s in required if s not in content]
    if missing:
        print("FAIL: Orchestrator script is missing identifiers: " + ", ".join(missing))
        sys.exit(1)
    print("PASS: Orchestrator script exists and contains core classes/identifiers.")
    sys.exit(0)

if __name__ == "__main__":
    run()
