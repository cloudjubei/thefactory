import os, sys

def run():
    path = "docs/AGENT_PLANNER.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    required_strings = [
        "docs/tasks/task_format.py",
        "docs/tasks/task_example.json",
        "create_task(task:Task)->Task",
        "create_feature(feature:Feature)->Feature",
        "update_task(id:int,title:str,action:str,plan:str)->Task",
        "update_feature(task_id:int,feature_id:str,title:str,action:str,context:[str],plan:str)->Feature",
        "The document explains that creating a task with features that clearly describe the full scope of the task is mandatory - `create_task` tool is used for this",
        "The document explains that creating features that are missing for the task to be complete is mandatory - `create_feature` tool is used for this",
        "The document explains that the task requires a generic high level plan - `update_task` tool is used for this",
        "The document explains that each feature requires a step-by-step plan that should make it easy to implement for an LLM - `update_feature` tool is used for this",
        "The document explains that each feature requires gathering a minimal context that is required per feature - `update_feature` tool is used for this",
    ]

    missing = [s for s in required_strings if s not in content]
    if missing:
        print("FAIL: Missing required content: " + ", ".join(missing))
        sys.exit(1)

    print("PASS: AGENT_PLANNER.md meets the acceptance criteria for feature 1.5.")
    sys.exit(0)

if __name__ == "__main__":
    run()
