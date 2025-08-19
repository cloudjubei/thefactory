import os, sys

def run_test():
    path = "scripts/run_local_agent.py"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    content = open(path, "r", encoding="utf-8").read()
    required_any = [
        "class Agent",  # core entry class
        "class AgentTools",  # tool facade
    ]
    tool_refs = [
        "def write_file(",
        "def retrieve_context_files(",
        "def rename_files(",
        "def submit_for_review(",
        "def ask_question(",
        "def finish(",
    ]
    if not all(s in content for s in required_any):
        print("FAIL: Orchestrator missing core classes (Agent/AgentTools).")
        sys.exit(1)
    # at least mention each tool method name in AgentTools
    missing_tools = [t for t in tool_refs if t not in content]
    if missing_tools:
        print(f"FAIL: Orchestrator missing tool bindings: {', '.join(missing_tools)}")
        sys.exit(1)
    print("PASS: Task 7 acceptance verified.")
    sys.exit(0)

if __name__ == "__main__":
    run_test()
