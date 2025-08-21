import os
import sys


def check_file(path, required_substrings):
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    missing = [s for s in required_substrings if s not in content]
    if missing:
        print(f"FAIL: {path} is missing required phrases: " + ", ".join(missing))
        sys.exit(1)


def run():
    check_file(
        "docs/AGENT_PERSONAS_PLANNER.md",
        [
            "looks at the task description",
            "creates a plan for completing a task",
            "can edit the plan descriptions",
        ],
    )
    check_file(
        "docs/AGENT_PERSONAS_TESTER.md",
        [
            "looks at the task description",
            "for each feature creates the most appropriate acceptance criteria",
            "creates a test case for each feature",
            "can edit the tests - no one else can",
        ],
    )
    check_file(
        "docs/AGENT_PERSONAS_DEVELOPER.md",
        [
            "looks at the task description",
            "for each feature, looks at the acceptance criteria",
            "develops the necesary result that satisfies the acceptance criteria",
            "They can never edit tests or acceptance criteria",
        ],
    )
    print("PASS: Agent personas files exist with required descriptions.")
    sys.exit(0)


if __name__ == "__main__":
    run()
