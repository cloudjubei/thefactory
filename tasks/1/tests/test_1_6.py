import os


def read_file(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def repo_root_from_here() -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    return os.path.abspath(os.path.join(here, '../../../'))


def test_agent_planner_md_exists_and_content():
    root = repo_root_from_here()
    doc_path = os.path.join(root, 'docs', 'AGENT_PLANNER.md')
    assert os.path.exists(doc_path), 'docs/AGENT_PLANNER.md must exist.'

    content = read_file(doc_path)

    # Must reference required files
    for needed in [
        'docs/tasks/task_format.py',
        'docs/tasks/task_example.json',
        'docs/AGENT_COMMUNICATION_PROTOCOL.md',
        'docs/agent_protocol_example.json',
    ]:
        assert needed in content, f'Missing required reference: {needed}'

    # Must describe the agent purpose per acceptance
    purpose_phrase = (
        'agent that looks at the task description and creates a plan for '
        'completing a task following the given specifications'
    )
    assert purpose_phrase in content, 'Document must describe the planner agent purpose.'

    # Tools section with exact signatures
    required_tools = [
        'create_task(task:Task)->Task',
        'create_feature(feature:Feature)->Feature',
        'update_task(id:int,title:str,action:str,plan:str)->Task',
        'update_feature(task_id:int,feature_id:str,title:str,action:str,context:[str],plan:str)->Feature',
        'update_agent_question(task_id:int,feature_id:str?,question:str)',
    ]
    for tool_sig in required_tools:
        assert tool_sig in content, f'Missing tool signature: {tool_sig}'

    # Mandated explanations (verbatim from acceptance criteria)
    required_explanations = [
        'The document explains that creating a task with features that clearly describe the full scope of the task is mandatory - `create_task` tool is used for this',
        'The document explains that creating features that are missing for the task to be complete is mandatory - `create_feature` tool is used for this',
        'The document explains that the task requires a generic high level plan - `update_task` tool is used for this',
        'The document explains that each feature requires a step-by-step plan that should make it easy to implement for an LLM - `update_feature` tool is used for this',
        'The document explains that each feature requires gathering a minimal context that is required per feature - `update_feature` tool is used for this',
        'The document explains that if there\'s any unresolved issue - the `update_agent_question` tool is used for this',
    ]
    for line in required_explanations:
        assert line in content, f'Missing mandated explanation: {line}'


def main():
    test_agent_planner_md_exists_and_content()
    print('PASS: Feature 1.6 AGENT_PLANNER.md meets acceptance criteria.')


if __name__ == '__main__':
    main()
