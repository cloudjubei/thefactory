import os, sys

def run():
    path = "docs/AGENT_PRINCIPLES.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if "The Agent" not in content or "The Orchestrator" not in content:
        print("FAIL: AGENT_PRINCIPLES.md missing required terminology.")
        sys.exit(1)
    print("PASS: Task 6 acceptance verified.")
    sys.exit(0)

if __name__ == "__main__":
    run()
