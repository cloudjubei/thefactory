import json
import sys
import os

def run():
    # 1. Check schema file for corrections
    schema_file = 'docs/tasks/task_format.py'
    if not os.path.exists(schema_file):
        print(f"FAIL: Schema file {schema_file} does not exist.")
        sys.exit(1)
        
    with open(schema_file, 'r', encoding='utf-8') as f:
        schema_content = f.read()

    if 'class AcceptanceCriterion(TypedDict):' not in schema_content:
        print("FAIL: AcceptanceCriterion TypedDict not found in schema.")
        sys.exit(1)

    if 'class Task(TypedDict):' not in schema_content:
        print("FAIL: Task TypedDict not found in schema.")
        sys.exit(1)

    if 'id: int' not in schema_content:
        print("FAIL: Task id is not of type int in schema.")
        sys.exit(1)

    if 'acceptance: List[AcceptanceCriterion]' not in schema_content:
        print("FAIL: Task acceptance field is missing or has wrong type in schema.")
        sys.exit(1)
    
    # 2. Check an actual task file against the schema's intent
    task_file = 'tasks/13/task.json'
    if not os.path.exists(task_file):
        print(f"FAIL: Task file {task_file} not found.")
        sys.exit(1)

    with open(task_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not isinstance(data.get('id'), int):
        print(f"FAIL: Task id in {task_file} is not an integer.")
        sys.exit(1)
        
    if 'acceptance' not in data:
        print(f"FAIL: Task {task_file} is missing 'acceptance' field.")
        sys.exit(1)
        
    if not isinstance(data.get('acceptance'), list):
        print(f"FAIL: Task 'acceptance' in {task_file} is not a list.")
        sys.exit(1)

    # 3. Check docs/TOOL_ARCHITECTURE.md for update
    doc_file = 'docs/TOOL_ARCHITECTURE.md'
    if not os.path.exists(doc_file):
        print(f"FAIL: Doc file {doc_file} does not exist.")
        sys.exit(1)
        
    with open(doc_file, 'r', encoding='utf-8') as f:
        doc_content = f.read()
    
    if 'TASKS.md' in doc_content:
        print("FAIL: docs/TOOL_ARCHITECTURE.md still contains reference to TASKS.md")
        sys.exit(1)
        
    print("PASS: Task schema, example, and documentation are consistent.")
    sys.exit(0)

if __name__ == "__main__":
    run()
