import os, sys

def run():
    path = "docs/PLAN_SPECIFICATION_PLANNER.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    required_strings = [
        "docs/tasks/task_format.py",
        "docs/tasks/task_example.json",
        "docs/tasks/TASKS_GUIDANCE.md",
        "docs/TOOL_ARCHITECTURE.md",
        "docs/AGENT_PRINCIPLES.md",
        "docs/AGENT_PERSONAS_PLANNER.md",
        "creating a task with features that clearly describe the full scope of the task is mandatory",
        "the task requires a generic high level plan",
        "each feature requires a step-by-step plan that should make it easy to implement for an LLM",
        "each feature requires gathering a minimal context that is required per feature",
    ]

    missing = [s for s in required_strings if s not in content]
    if missing:
        print("FAIL: PLAN_SPECIFICATION_PLANNER.md missing required items: " + ", ".join(missing))
        sys.exit(1)

    print("PASS: PLAN_SPECIFICATION_PLANNER.md meets acceptance criteria for feature 1.10.")
    sys.exit(0)

if __name__ == "__main__":
    run()
