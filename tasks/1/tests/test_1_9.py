import os
import sys

def run():
    file_path = "docs/AGENT_PERSONAS.md"
    print(f"--- Running Test for Feature 1.9: Agent Personas ---")

    if not os.path.exists(file_path):
        print(f"FAIL: File '{file_path}' does not exist.")
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    required_personas = [
        "Persona 1: Planner",
        "Persona 2: Tester",
        "Persona 3: Developer"
    ]

    missing_personas = [p for p in required_personas if p not in content]

    if missing_personas:
        print(f"FAIL: Missing persona definitions in '{file_path}': {', '.join(missing_personas)}")
        sys.exit(1)

    print(f"PASS: '{file_path}' exists and contains all required persona definitions.")
    sys.exit(0)

if __name__ == "__main__":
    run()
