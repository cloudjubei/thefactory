import os
import sys

def run_test():
    """
    Verifies the acceptance criteria for feature 1.8.
    """
    file_path = "docs/AGENT_DEVELOPER.md"
    errors = []

    # 1. Check if file exists
    if not os.path.exists(file_path):
        errors.append(f"FAIL: File '{file_path}' does not exist.")
        print("\n".join(errors))
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 2. Check for references
    expected_references = [
        "`docs/AGENT_PERSONAS_DEVELOPER.md`",
        "`docs/FILE_ORGANISATION.md`",
        "`docs/AGENT_COMMUNICATION_PROTOCOL.md`",
        "`docs/agent_protocol_format.json`"
    ]
    for ref in expected_references:
        if ref not in content:
            errors.append(f"FAIL: Missing reference to '{ref}'.")

    # 3. Check for Tools section
    if "## Tools" not in content:
        errors.append("FAIL: Missing '## Tools' section.")

    # 4. Check for all tools
    expected_tools = [
        "`get_context(files:[str])->[str]`",
        "`write_file(filename:str,content:str)`",
        "`run_test(task_id:int,feature_id:str)->TestResult`",
        "`update_task_status(task_id:int,status:Status)->Task`",
        "`update_feature_status(task_id:int,feature_id:str,status:Status)->Feature`",
        "`finish_feature(task_id:int,feature_id:str)->Feature`",
        "`finish(task_id:int)->Task`",
        "`update_agent_question(task_id:int,feature_id:str?,question:str)`"
    ]
    for tool in expected_tools:
        if tool not in content:
            errors.append(f"FAIL: Missing tool signature: {tool}.")

    # 5. Check for workflow explanations
    workflow_explanations = [
        "task status is updated to in progress",
        "feature that is worked on the status is updated to in progress",
        "context needs to be gathered",
        "plan needs to be carried out",
        "task isn't deemed done until all tests pass",
        "status needs to be updated when work is finished",
        "`finish_feature` MUST BE USED",
        "`finish` MUST BE USED",
        "if there's any unresolved issue"
    ]
    content_lower = content.lower()
    for explanation in workflow_explanations:
        if explanation.lower() not in content_lower:
            errors.append(f"FAIL: Missing workflow explanation: '{explanation}'.")

    if errors:
        print("\n".join(errors))
        sys.exit(1)
    else:
        print(f"PASS: All acceptance criteria for feature 1.8 met.")
        sys.exit(0)

if __name__ == "__main__":
    run_test()
