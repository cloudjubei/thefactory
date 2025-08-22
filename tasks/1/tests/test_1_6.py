import os
import re

def test_feature_1_6():
    doc_path = 'docs/AGENT_PLANNER.md'
    assert os.path.exists(doc_path), 'docs/AGENT_PLANNER.md does not exist'
    with open(doc_path, 'r') as f:
        content = f.read()
    # Check references
    assert 'docs/tasks/task_format.py' in content
    assert 'docs/tasks/task_example.json' in content
    assert 'docs/AGENT_COMMUNICATION_PROTOCOL.md' in content
    assert 'docs/agent_response_example.json' in content
    # Check Tools section
    assert re.search(r'#\s*Tools', content) or 'Tools' in content
    # Check tool signatures
    assert 'create_task(task:Task)->Task' in content
    assert 'create_feature(feature:Feature)->Feature' in content
    assert 'update_task(id:int,title:str,action:str,plan:str)->Task' in content
    assert 'update_feature(task_id:int,feature_id:str,title:str,action:str,context:[str],plan:str)->Feature' in content
    assert 'block_feature(task_id:int,feature_id:str,reason:str)' in content
    # Check explanation phrases
    assert 'creating a task with features that clearly describe the full scope of the task is mandatory' in content
    assert 'creating features that are missing for the task to be complete is mandatory' in content
    assert 'task requires a generic high level plan' in content
    assert 'each feature requires a step-by-step plan that should make it easy to implement for an LLM' in content
    assert 'each feature requires gathering a minimal context that is required per feature' in content
    assert "if there's any unresolved issue - the `block_feature` tool is used for this" in content
    # Check agent description
    assert 'agent that looks at the task description and creates a plan for completing a task following the given specifications' in content