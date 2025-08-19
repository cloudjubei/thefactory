import os, sys

def run():
    personas_doc = "docs/AGENT_PERSONAS.md"
    orchestrator = "scripts/run_local_agent.py"

    # Check personas doc
    if not os.path.exists(personas_doc):
        print(f"FAIL: {personas_doc} does not exist.")
        sys.exit(1)
    with open(personas_doc, "r", encoding="utf-8") as f:
        personas_content = f.read()

    required_personas = ["Manager", "Planner", "Tester", "Developer"]
    missing = [p for p in required_personas if p not in personas_content]
    if missing:
        print("FAIL: AGENT_PERSONAS.md missing personas: " + ", ".join(missing))
        sys.exit(1)

    # Check orchestrator persona support
    if not os.path.exists(orchestrator):
        print(f"FAIL: {orchestrator} does not exist.")
        sys.exit(1)
    with open(orchestrator, "r", encoding="utf-8") as f:
        code = f.read()

    # argparse choices for persona
    if "--persona" not in code or "choices=['manager', 'planner', 'tester', 'developer']" not in code:
        print("FAIL: run_local_agent.py does not expose --persona with required choices.")
        sys.exit(1)

    # Presence of persona instruction blocks and minimal context branches
    needed_snippets = [
        "You are the Manager persona.",
        "You are the Planner persona.",
        "You are the Tester persona.",
        "You are the Developer persona.",
        "elif persona == 'manager':",
        "elif persona == 'planner':",
        "elif persona == 'tester':",
        "elif persona == 'developer':",
    ]
    missing_snips = [s for s in needed_snippets if s not in code]
    if missing_snips:
        print("FAIL: run_local_agent.py missing persona support elements: " + ", ".join(missing_snips))
        sys.exit(1)

    print("PASS: Personas documented and orchestrator supports persona mode with minimal context.")
    sys.exit(0)

if __name__ == "__main__":
    run()
