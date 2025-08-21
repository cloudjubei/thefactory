import os
import sys

def run():
    """
    Test for Task 1, Feature 1.10: Plan Specification Document (Revised for robustness)
    """
    file_path = "docs/PLAN_SPECIFICATION.md"
    errors = []

    if not os.path.exists(file_path):
        print(f"FAIL: File '{file_path}' does not exist.")
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    content_lower = content.lower()

    # Check for required references
    references = [
        "docs/tasks/task_format.py",
        "docs/tasks/task_example.json",
        "docs/tasks/TASKS_GUIDANCE.md",
        "docs/TESTING.md",
        "docs/TOOL_ARCHITECTURE.md",
        "docs/AGENT_PRINCIPLES.md",
        "docs/AGENT_PERSONAS.md",
    ]
    for ref in references:
        if ref not in content:
            errors.append(f"FAIL: Document is missing reference to '{ref}'.")

    # Check for key concepts using keyword groups (all must be present)
    concept_checks = {
        "full scope": ["full scope", "features"],
        "high-level plan": ["generic", "high-level plan"],
        "feature plan": ["feature", "step-by-step"],
        "acceptance criteria": ["rigorous", "acceptance criteria"],
        "status updates": ["status", "update", "`write_file`"],
        "feature completion": ["feature", "complete", "`finish_feature`"],
        "task completion": ["task", "complete", "`submit_for_review`", "`finish`"],
    }

    for concept, keywords in concept_checks.items():
        if not all(keyword in content_lower for keyword in keywords):
            errors.append(f"FAIL: Document does not seem to explain the concept of '{concept}'. Missing one of: {keywords}")

    if errors:
        print(f"FAIL: Test for feature 1.10 failed. Found {len(errors)} issues in {file_path}:")
        for error in errors:
            print(f"- {error}")
        sys.exit(1)
    else:
        print("PASS: docs/PLAN_SPECIFICATION.md meets all acceptance criteria for feature 1.10.")
        sys.exit(0)

if __name__ == "__main__":
    run()
