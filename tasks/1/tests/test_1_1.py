import os
import sys
import inspect
from typing import TypedDict, List, Optional

def run():
    print("Running test for Feature 1.1: Canonical Task Schema...")
    
    # 1. Check for file existence
    file_path = "docs/tasks/task_format.py"
    if not os.path.exists(file_path):
        print(f"FAIL: {file_path} does not exist.")
        sys.exit(1)
    
    # 2. Check for TypedDict definitions
    # Add the directory to the path to allow importing
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../docs/tasks')))
    
    try:
        from task_format import Task, Feature
    except ImportError as e:
        print(f"FAIL: Could not import Task and Feature from {file_path}. Error: {e}")
        sys.exit(1)
    finally:
        sys.path.pop(0)

    if not (hasattr(Task, '__annotations__') and hasattr(Feature, '__annotations__')):
        print("FAIL: Task or Feature is not a TypedDict or is not defined correctly.")
        sys.exit(1)
        
    # 3. Check for required fields
    required_task_fields = ['id', 'status', 'title', 'action', 'plan', 'features']
    required_feature_fields = ['id', 'status', 'title', 'action', 'plan', 'context', 'acceptance']
    
    task_annotations = Task.__annotations__
    feature_annotations = Feature.__annotations__
    
    missing_task_fields = [f for f in required_task_fields if f not in task_annotations]
    if missing_task_fields:
        print(f"FAIL: Task schema is missing required fields: {', '.join(missing_task_fields)}")
        sys.exit(1)
        
    missing_feature_fields = [f for f in required_feature_fields if f not in feature_annotations]
    if missing_feature_fields:
        print(f"FAIL: Feature schema is missing required fields: {', '.join(missing_feature_fields)}")
        sys.exit(1)
        
    print("PASS: docs/tasks/task_format.py exists and defines a valid Task and Feature schema.")
    sys.exit(0)

if __name__ == "__main__":
    run()
