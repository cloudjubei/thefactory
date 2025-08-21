import os
import sys

def run():
    file_path = "docs/AGENT_PRINCIPLES.md"
    print(f"--- Running Test for Feature 1.8: Principles Guide ---")

    if not os.path.exists(file_path):
        print(f"FAIL: File '{file_path}' does not exist.")
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    reference = "docs/TOOL_ARCHITECTURE.md"
    if reference not in content:
        print(f"FAIL: The file does not reference '{reference}' as required.")
        sys.exit(1)

    print(f"PASS: '{file_path}' exists and references the tools guide.")
    sys.exit(0)

if __name__ == "__main__":
    run()
