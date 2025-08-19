import os, sys

def run():
    doc = "docs/AGENT_PRINCIPLES.md"
    if not os.path.exists(doc):
        print(f"FAIL: {doc} does not exist.")
        sys.exit(1)
    with open(doc, "r", encoding="utf-8") as f:
        c = f.read()
    if "The Agent" not in c or "The Orchestrator" not in c:
        print("FAIL: AGENT_PRINCIPLES.md missing core terminology.")
        sys.exit(1)
    print("PASS: AGENT_PRINCIPLES.md exists with key terms.")
    sys.exit(0)

if __name__ == "__main__":
    run()
