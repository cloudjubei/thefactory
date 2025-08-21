import os
import ast
import inspect
import importlib.util

def test_task_utils_exists():
    assert os.path.exists('scripts/task_utils.py')

def test_imports():
    with open('scripts/task_utils.py', 'r') as f:
        tree = ast.parse(f.read())
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            module = node.module
            names = [alias.name for alias in node.names]
            imports.append((module, names))
    has_task_feature = any(module == 'docs.tasks.task_format' and ('Task' in names and 'Feature' in names) for module, names in imports)
    assert has_task_feature, "Missing import of Task and Feature from docs/tasks/task_format.py"
    has_git_manager = any(module == 'scripts.git_manager' and 'GitManager' in names for module, names in imports)
    assert has_git_manager, "Missing import of GitManager from scripts/git_manager.py"

def test_function_definitions():
    spec = importlib.util.spec_from_file_location("task_utils", 'scripts/task_utils.py')
    task_utils = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(task_utils)
    functions = {
        'update_feature_plan': ['task_id', 'feature_id', 'plan', 'git_manager'],
        'create_feature': ['task_id', 'feature', 'git_manager'],
        'finish_feature': ['task_id', 'feature_id', 'git_manager'],
        'block_feature': ['task_id', 'feature_id', 'reason', 'git_manager'],
        'update_acceptance_criteria': ['task_id', 'feature_id', 'criteria', 'git_manager'],
        'update_test': ['task_id', 'feature_id', 'test', 'git_manager'],
        'run_test': ['task_id', 'feature_id'],
        'write_file': ['filename', 'content', 'git_manager'],
        'get_context': ['files'],
    }
    for func_name, params in functions.items():
        assert hasattr(task_utils, func_name), f"Missing function {func_name}"
        func = getattr(task_utils, func_name)
        assert callable(func), f"{func_name} is not callable"
        sig = inspect.signature(func)
        actual_params = list(sig.parameters.keys())
        assert actual_params == params, f"Signature mismatch for {func_name}: expected {params}, got {actual_params}"

# Note: Testing the behavioral criteria (respecting file format) would require functional tests with mocks, which can be added separately.