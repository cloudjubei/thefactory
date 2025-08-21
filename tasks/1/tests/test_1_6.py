import os
import sys

def run_test():
    """
    Verifies the acceptance criteria for feature 1.6.
    """
    file_path = "docs/AGENT_PLANNER.md"
    errors = []

    # 1. Check if file exists
    if not os.path.exists(file_path):
        errors.append(f"FAIL: File '{file_path}' does not exist.")
        print("\n".join(errors))
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 2. Check for key sections and references
    expected_references = [
        "`docs/tasks/task_format.py`",
        "`docs/tasks/task_example.json`",
        "`docs/AGENT_COMMUNICATION_PROTOCOL.md`",
        "`docs/agent_protocol_format.json`"
    ]
    for ref in expected_references:
        if ref not in content:
            errors.append(f"FAIL: Missing reference to '{ref}'.")

    # 3. Check for Tools section and specific tools
    if "## Tools" not in content:
        errors.append("FAIL: Missing '## Tools' section.")

    expected_tools = [
        "`create_task(task:Task)->Task`",
        "`create_feature(feature:Feature)->Feature`",
        "`update_task(id:int,title:str,action:str,plan:str)->Task`",
        "`update_feature(task_id:int,feature_id:str,title:str,action:str,context:[str],plan:str)->Feature`",
        "`update_agent_question(task_id:int,feature_id:str?,question:str)`"
    ]

    for tool in expected_tools:
        if tool not in content:
            errors.append(f"FAIL: Missing tool signature: {tool}.")

    # 4. Check for workflow explanations
    workflow_keywords = [
        "creating a task with features that clearly describe the full scope of the task is mandatory",
        "creating features that are missing for the task to be complete is mandatory",
        "task requires a generic high level plan",
        "feature requires a step-by-step plan",
        "feature requires gathering a minimal context"
    ]
    for keyword in workflow_keywords:
        if keyword not in content.lower():
            errors.append(f"FAIL: Missing explanation for workflow keyword: '{keyword}'.")


    if errors:
        print("\n".join(errors))
        sys.exit(1)
    else:
        print("PASS: All acceptance criteria for feature 1.6 met.")
        sys.exit(0)

if __name__ == "__main__":
    run_test()
