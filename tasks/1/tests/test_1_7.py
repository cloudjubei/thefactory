import os
import sys

def run():
    file_path = "docs/TOOL_ARCHITECTURE.md"
    print(f"--- Running Test for Feature 1.7: Tools Guide ---")

    if not os.path.exists(file_path):
        print(f"FAIL: File '{file_path}' does not exist.")
        sys.exit(1)
        
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    required_sections = [
        "Core Principle",
        "Agent-Orchestrator Contract",
        "JSON Response Schema",
        "Available Tools",
        "Execution Modes",
        "Mandatory Task Completion Workflow"
    ]

    missing_sections = [s for s in required_sections if s not in content]

    if missing_sections:
        print(f"FAIL: Missing sections in '{file_path}': {', '.join(missing_sections)}")
        sys.exit(1)

    print(f"PASS: '{file_path}' exists and seems to have the required sections.")
    sys.exit(0)

if __name__ == "__main__":
    run()
