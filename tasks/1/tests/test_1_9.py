import os
def test_contexter_spec():
    file_path = 'docs/AGENT_CONTEXTER.md'
    assert os.path.exists(file_path), 'docs/AGENT_CONTEXTER.md does not exist'
    with open(file_path, 'r') as f:
        content = f.read()
    assert 'docs/FILE_ORGANISATION.md' in content, 'No reference to docs/FILE_ORGANISATION.md'
    assert 'Tools' in content, 'No Tools section'
    tools = [
        'get_context(files:[str])->[str]',
        'update_feature_context(task_id:int,feature_id:str,context:[str])->Feature',
        'finish_feature(task_id:int,feature_id:str)->Feature',
        'block_feature(task_id:int,feature_id:str,question:str)'
    ]
    for tool in tools:
        assert tool in content, f'Tool {tool} not listed'
    assert 'minimal file context' in content.lower() and 'update_feature_context' in content, 'Missing explanation for minimal context and update_feature_context'
    assert 'docs/FILE_ORGANISATION.md' in content and 'get_context' in content, 'Missing explanation for using FILE_ORGANISATION.md and get_context for extra context'
    assert 'finish_feature MUST BE USED' in content, 'Missing explanation for finish_feature'
    assert 'unresolved issue' in content.lower() and 'block_feature' in content, 'Missing explanation for block_feature'