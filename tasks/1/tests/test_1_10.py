import os
import sys

def run():
    file_path = "docs/PLAN_SPECIFICATION.md"
    print(f"--- Running Test for Feature 1.10: Plan Specification ---")
    
    if not os.path.exists(file_path):
        print(f"FAIL: File '{file_path}' does not exist.")
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    all_required_references = [
        "docs/tasks/task_format.py",
        "docs/tasks/task_example.json",
        "docs/tasks/TASKS_GUIDANCE.md",
        "docs/TESTING.md",
        "docs/TOOL_ARCHITECTURE.md",
        "docs/AGENT_PRINCIPLES.md",
        "docs/AGENT_PERSONAS.md",
    ]

    missing_references = [ref for ref in all_required_references if ref not in content]
    if missing_references:
        print(f"FAIL: Missing references in '{file_path}': {', '.join(missing_references)}")
        sys.exit(1)

    required_explanations = [
        "full scope of the task is mandatory",
        "generic high level plan",
        "step-by-step plan",
        "rigorous acceptance criteria",
        "`write_file` tool",
        "`finish_feature` tool",
        "`submit_for_review` tool"
    ]
    
    missing_explanations = [exp for exp in required_explanations if exp not in content]
    if missing_explanations:
        print(f"FAIL: Missing explanations in '{file_path}': {', '.join(missing_explanations)}")
        sys.exit(1)

    print(f"PASS: '{file_path}' exists and meets all acceptance criteria.")
    sys.exit(0)

if __name__ == "__main__":
    run()
