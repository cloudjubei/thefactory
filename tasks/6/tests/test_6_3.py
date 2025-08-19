import os, sys

def run():
    path = "docs/AGENT_PRINCIPLES.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    required = [
        "# Autonomous Agent Principles",
        "The Agent",
        "The Orchestrator",
        "Core Principles"
    ]
    missing = [s for s in required if s not in content]
    if missing:
        print("FAIL: Missing required content in AGENT_PRINCIPLES.md: " + ", ".join(missing))
        sys.exit(1)
    print("PASS: AGENT_PRINCIPLES.md exists and contains required sections/terms.")
    sys.exit(0)

if __name__ == "__main__":
    run()
