import os
import sys

def run():
    path = os.path.join("docs", "AGENT_PRINCIPLES.md")
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if "The Agent" not in content or "The Orchestrator" not in content:
        print("FAIL: AGENT_PRINCIPLES.md missing key terminology.")
        sys.exit(1)

    print("PASS: AGENT_PRINCIPLES.md exists and defines key terms.")
    sys.exit(0)

if __name__ == "__main__":
    run()
