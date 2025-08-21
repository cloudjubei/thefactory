import os
import sys
import importlib.util
from typing import TypedDict, List

# Check if file exists
assert os.path.exists('docs/tasks/task_format.py'), "File does not exist"

# Load the module
spec = importlib.util.spec_from_file_location("task_format", 'docs/tasks/task_format.py')
task_format = importlib.util.module_from_spec(spec)
sys.modules['task_format'] = task_format
spec.loader.exec_module(task_format)

# Check for Task and Feature
assert hasattr(task_format, 'Task'), "Task not defined"
assert hasattr(task_format, 'Feature'), "Feature not defined"
assert issubclass(task_format.Task, TypedDict), "Task is not a TypedDict"
assert issubclass(task_format.Feature, TypedDict), "Feature is not a TypedDict"

# Check Task fields
task_fields = task_format.Task.__annotations__
expected_task_fields = {
    'id': str,
    'title': str,
    'features': List[task_format.Feature],
}
assert set(task_fields.keys()) == set(expected_task_fields.keys()), "Task fields do not match"
for field, typ in expected_task_fields.items():
    assert task_fields[field] == typ, f"Type mismatch for Task.{field}: expected {typ}, got {task_fields[field]}"

# Check Feature fields
feature_fields = task_format.Feature.__annotations__
expected_feature_fields = {
    'id': str,
    'title': str,
    'description': str,
    'acceptance_criteria': List[str],
}
assert set(feature_fields.keys()) == set(expected_feature_fields.keys()), "Feature fields do not match"
for field, typ in expected_feature_fields.items():
    assert feature_fields[field] == typ, f"Type mismatch for Feature.{field}: expected {typ}, got {feature_fields[field]}"
