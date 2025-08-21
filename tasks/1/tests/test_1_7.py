import os
import sys

def run_test():
    """
    Verifies the acceptance criteria for feature 1.7.
    """
    file_path = "docs/AGENT_TESTER.md"
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
        "`docs/AGENT_PERSONAS_TESTER.md`",
        "`docs/TESTING.md`",
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
        "`get_test(task_id:int,feature_id:str)->str?`",
        "`update_acceptance_criteria(task_id:int,feature_id:str,acceptance_criteria:[str])->Feature`",
        "`update_test(task_id:int,feature_id:str,test:str)`",
        "`delete_test(task_id:int,feature_id:str)`",
        "`run_test(task_id:int,feature_id:str)->TestResult`",
        "`update_task_status(task_id:int,status:Status)->Task`",
        "`update_feature_status(task_id:int,feature_id:str,status:Status)->Feature`",
        "`update_agent_question(task_id:int,feature_id:str?,question:str)`"
    ]
    for tool in expected_tools:
        if tool not in content:
            errors.append(f"FAIL: Missing tool signature: {tool}.")

    # 5. Check for workflow explanations
    if "rigorous and atomic acceptance criteria" not in content:
        errors.append("FAIL: Missing explanation for 'update_acceptance_criteria'.")
    if "tests written that match each acceptance criteria" not in content:
        errors.append("FAIL: Missing explanation for 'update_test'/'delete_test'.")
    if "tester can run tests" not in content:
        errors.append("FAIL: Missing explanation for 'run_test'.")
    if "task status needs to be updated when work is not finished" not in content:
        errors.append("FAIL: Missing explanation for 'update_task_status'.")
    if "feature status needs to be updated when work is not finished" not in content:
        errors.append("FAIL: Missing explanation for 'update_feature_status'.")
    if "if there's any unresolved issue" not in content:
        errors.append("FAIL: Missing explanation for 'update_agent_question'.")

    if errors:
        print("\n".join(errors))
        sys.exit(1)
    else:
        print(f"PASS: All acceptance criteria for feature 1.7 met.")
        sys.exit(0)

if __name__ == "__main__":
    run_test()
