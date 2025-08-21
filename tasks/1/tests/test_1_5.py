import os
import json

def test_agent_communication_protocol():
    md_path = 'docs/AGENT_COMMUNICATION_PROTOCOL.md'
    json_path = 'docs/agent_response_example.json'
    
    assert os.path.exists(md_path), f"{md_path} does not exist"
    with open(md_path, 'r') as f:
        md_content = f.read()
    assert len(md_content.strip()) > 0, "MD file is empty"
    
    assert os.path.exists(json_path), f"{json_path} does not exist"
    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
            assert isinstance(data, dict), "JSON is not an object"
            assert 'thoughts' in data, "Missing 'thoughts' key"
            assert 'tool_calls' in data, "Missing 'tool_calls' key"
            assert isinstance(data['tool_calls'], list), "'tool_calls' is not a list"
        except json.JSONDecodeError:
            assert False, "Invalid JSON"