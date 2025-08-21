import os


def test_agent_tester_doc_exists_and_has_required_content():
    path = os.path.join('docs', 'AGENT_TESTER.md')
    assert os.path.isfile(path), 'docs/AGENT_TESTER.md must exist'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Must reference core guidance and protocol docs
    assert 'docs/TESTING.md' in content, 'Must reference docs/TESTING.md'
    assert 'docs/AGENT_COMMUNICATION_PROTOCOL.md' in content, 'Must reference docs/AGENT_COMMUNICATION_PROTOCOL.md'
    assert 'docs/agent_protocol_example.json' in content, 'Must reference docs/agent_protocol_example.json'

    # Must have a Tools section and list all required tools
    assert 'Tools' in content, 'Must contain a Tools section'
    required_tools = [
        'get_test(',
        'update_acceptance_criteria(',
        'update_test(',
        'delete_test(',
        'run_test(',
        'update_task_status(',
        'update_feature_status(',
        'update_agent_question('
    ]
    for tool in required_tools:
        assert tool in content, f'Missing tool specification: {tool}'

    # Must explain key expectations per acceptance criteria
    assert 'rigorous and atomic acceptance criteria' in content, 'Must explain rigorous and atomic acceptance criteria'
    assert 'context' in content and 'get_test' in content, 'Must explain gathering minimal context with get_test'
    assert 'run_test' in content and 'execute' in content, 'Must explain that the tester can run tests using run_test'
    assert 'update_task_status' in content and 'update_feature_status' in content and 'not finished' in content, 'Must explain status updates when work is not finished'
    assert 'update_agent_question' in content and 'unresolved' in content, 'Must explain how to raise unresolved issues via update_agent_question'
