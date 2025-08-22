import os
import importlib.util
import sys

# Check file exists
assert os.path.exists('docs/tasks/task_format.py'), "File does not exist"

# Load the module
spec = importlib.util.spec_from_file_location("task_format", "docs/tasks/task_format.py")
task_format = importlib.util.module_from_spec(spec)
sys.modules["task_format"] = task_format
spec.loader.exec_module(task_format)

# Check Task is defined
assert hasattr(task_format, 'Task'), "Task not defined"

Task = task_format.Task
assert issubclass(Task, dict), "Task is not a subclass of dict"
assert hasattr(Task, '__annotations__'), "Task has no __annotations__"

task_annotations = Task.__annotations__
assert set(task_annotations.keys()) == {'id', 'title', 'features', 'status', 'description', 'rejection'}, "Task fields mismatch"
assert task_annotations['id'] is int, "id not int"
assert task_annotations['title'] is str, "title not str"

# For features: should be list[Feature]
features_type = task_annotations['features']
assert features_type.__origin__ is list, "features not list"
assert len(features_type.__args__) == 1, "features not list of single type"
assert features_type.__args__[0] is task_format.Feature, "features not list[Feature]"

# Now Feature
assert hasattr(task_format, 'Feature'), "Feature not defined"

Feature = task_format.Feature
assert issubclass(Feature, dict), "Feature not subclass of dict"
assert hasattr(Feature, '__annotations__'), "Feature has no __annotations__"

feature_annotations = Feature.__annotations__
assert set(feature_annotations.keys()) == {'id', 'status', 'title', 'description', 'plan', 'context', 'acceptance', 'dependencies', 'rejection'}, "Feature fields mismatch"
assert feature_annotations['id'] is str
assert feature_annotations['title'] is str
assert feature_annotations['description'] is str

ac_type = feature_annotations['acceptance']
assert ac_type.__origin__ is list
assert len(ac_type.__args__) == 1
assert ac_type.__args__[0] is str