import os
import sys
import json

def run():
    print("Running test for Feature 1.3: Example Task File...")
    
    schema_path = "docs/tasks/task_format.py"
    example_path = "docs/tasks/task_example.json"
    
    # 1. Check for file existence
    if not os.path.exists(example_path):
        print(f"FAIL: {example_path} does not exist.")
        sys.exit(1)

    if not os.path.exists(schema_path):
        print(f"FAIL: Schema file {schema_path} does not exist, cannot validate example.")
        sys.exit(1)
        
    # 2. Check for valid JSON
    try:
        with open(example_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"FAIL: {example_path} is not a valid JSON file. Error: {e}")
        sys.exit(1)
        
    # 3. Check for schema conformance (key check)
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../docs/tasks')))
    try:
        from task_format import Task, Feature
    except ImportError as e:
        print(f"FAIL: Could not import Task/Feature schema. Error: {e}")
        sys.exit(1)
    finally:
        sys.path.pop(0)

    # Check top-level task keys
    data_keys = set(data.keys())
    required_task_keys = {'id', 'status', 'title', 'action', 'plan', 'features'}
    
    if not required_task_keys.issubset(data_keys):
        print(f"FAIL: Example task is missing required keys: {required_task_keys - data_keys}")
        sys.exit(1)

    # Check feature keys
    if 'features' not in data or not isinstance(data['features'], list):
        print("FAIL: Example task 'features' key is missing or not a list.")
        sys.exit(1)
        
    required_feature_keys = {'id', 'status', 'title', 'action', 'plan', 'context', 'acceptance'}
    
    for i, feature in enumerate(data['features']):
        feature_data_keys = set(feature.keys())
        if not required_feature_keys.issubset(feature_data_keys):
            print(f"FAIL: Feature #{i+1} in example is missing required keys: {required_feature_keys - feature_data_keys}")
            sys.exit(1)

    print("PASS: docs/tasks/task_example.json exists, is valid JSON, and conforms to the Task schema.")
    sys.exit(0)

if __name__ == "__main__":
    run()
