import os, sys

def require(substrings, content, section):
    missing = [s for s in substrings if s not in content]
    if missing:
        print(f"FAIL: {section} missing required strings: " + ", ".join(missing))
        sys.exit(1)

def run():
    path = "docs/AGENT_TESTER.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # References
    require(["docs/AGENT_PERSONAS_TESTER.md", "docs/TESTING.md"], content, "References")

    # Tools presence with signatures
    tools = [
        "get_test(",
        "update_acceptance_criteria(",
        "update_test(",
        "delete_test(",
        "run_test(",
        "update_task_status(",
        "update_feature_status("
    ]
    require(tools, content, "Tools")

    # Context gathering guidance
    require(["required context", "get_test", "initial context"], content, "Context gathering guidance")

    # Acceptance criteria guidance
    require(["rigorous", "acceptance criteria", "update_acceptance_criteria"], content, "Acceptance criteria guidance")

    # Tests writing guidance
    require(["tests", "update_test", "delete_test"], content, "Tests writing guidance")

    # Running tests guidance
    require(["run_test"], content, "Running tests guidance")

    # Status update guidance
    require(["task status", "update_task_status"], content, "Task status guidance")
    require(["feature status", "update_feature_status"], content, "Feature status guidance")

    print("PASS: AGENT_TESTER.md exists with required content.")
    sys.exit(0)

if __name__ == "__main__":
    run()
