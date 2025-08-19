import os
import sys

def run():
    path = "docs/AGENT_PRINCIPLES.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    required_phrases = ["The Agent:", "The Orchestrator:"]
    missing = [p for p in required_phrases if p not in content]
    if missing:
        print("FAIL: AGENT_PRINCIPLES.md missing: " + ", ".join(missing))
        sys.exit(1)
    print("PASS: Task 6 - AGENT_PRINCIPLES.md defines Agent and Orchestrator.")
    sys.exit(0)

if __name__ == "__main__":
    run()
