import os
import re

def test_feature_1_8():
    doc_path = 'docs/AGENT_DEVELOPER.md'
    assert os.path.exists(doc_path), 'docs/AGENT_DEVELOPER.md does not exist'
    with open(doc_path, 'r') as f:
        content = f.read()
    assert 'docs/AGENT_DEVELOPER.md' in content, 'No reference to docs/AGENT_DEVELOPER.md'
    assert 'docs/FILE_ORGANISATION.md' in content, 'No reference to docs/FILE_ORGANISATION.md'
    assert 'docs/AGENT_COMMUNICATION_PROTOCOL.md' in content, 'No reference to docs/AGENT_COMMUNICATION_PROTOCOL.md'
    assert 'docs/agent_response_example.json' in content, 'No reference to docs/agent_response_example.json'
    assert 'Tools' in content, 'No Tools section'
    tools = ['get_context(files:[str])->[str]', 'write_file(filename:str,content:str)', 'run_test(task_id:int,feature_id:str)->TestResult', 'update_task_status(task_id:int,status:Status)->Task', 'update_feature_status(task_id:int,feature_id:str,status:Status)->Feature', 'finish_feature(task_id:int,feature_id:str)->Feature', 'finish(task_id:int)->Task', 'block_feature(task_id:int,feature_id:str,question:str)']
    for tool in tools:
        assert tool in content, f'Tool missing: {tool}'
    assert 'update_task_status' in content and 'in progress' in content, 'Missing explanation for task status update to in progress'
    assert 'update_feature_status' in content and 'in progress' in content, 'Missing explanation for feature status update to in progress'
    assert 'get_context' in content and 'very rare cases' in content, 'Missing explanation for context gathering'
    assert 'write_file' in content and 'writing any files' in content, 'Missing explanation for carrying out the plan'
    assert 'run_test' in content and 'all tests pass' in content, 'Missing explanation for tests passing'
    assert 'update_feature_status' in content and 'work is finished' in content, 'Missing explanation for updating feature status when finished'
    assert 'update_task_status' in content and 'work is finished' in content, 'Missing explanation for updating task status when finished'
    assert 'finish_feature' in content and 'MUST BE USED' in content, 'Missing explanation for finish_feature'
    assert 'finish' in content and 'MUST BE USED' in content, 'Missing explanation for finish'
    assert 'block_feature' in content and 'unresolved issue' in content, 'Missing explanation for block_feature'