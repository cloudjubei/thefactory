import os
import importlib.util
import inspect

def test_git_manager_feature():
    file_path = 'scripts/git_manager.py'
    assert os.path.exists(file_path), f"File {file_path} does not exist."

    spec = importlib.util.spec_from_file_location("git_manager", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    assert hasattr(module, 'GitManager'), "Class 'GitManager' not defined."

    GM = module.GitManager

    # Check __init__
    assert hasattr(GM, '__init__')
    init_sig = inspect.signature(GM.__init__)
    assert 'repo_path' in init_sig.parameters, "__init__ missing 'repo_path' parameter."
    repo_path_param = init_sig.parameters['repo_path']
    assert repo_path_param.default is inspect.Parameter.empty, "'repo_path' should be required (no default)."

    # Check clone
    assert hasattr(GM, 'clone')
    clone_sig = inspect.signature(GM.clone)
    assert 'url' in clone_sig.parameters, "clone missing 'url' parameter."
    url_param = clone_sig.parameters['url']
    assert url_param.default is inspect.Parameter.empty, "'url' should be required (no default)."
    assert 'path' in clone_sig.parameters, "clone missing 'path' parameter."
    path_param = clone_sig.parameters['path']
    assert path_param.default is inspect.Parameter.empty, "'path' should be required (no default)."

    # Check add
    assert hasattr(GM, 'add')
    add_sig = inspect.signature(GM.add)
    assert 'files' in add_sig.parameters, "add missing 'files' parameter."
    files_param = add_sig.parameters['files']
    assert files_param.default is not inspect.Parameter.empty, "'files' parameter should be optional (has default)."

    # Check commit
    assert hasattr(GM, 'commit')
    commit_sig = inspect.signature(GM.commit)
    assert 'message' in commit_sig.parameters, "commit missing 'message' parameter."
    message_param = commit_sig.parameters['message']
    assert message_param.default is inspect.Parameter.empty, "'message' should be required (no default)."

    # Check push
    assert hasattr(GM, 'push')
    push_sig = inspect.signature(GM.push)
    assert 'branch' in push_sig.parameters, "push missing 'branch' parameter."
    branch_param = push_sig.parameters['branch']
    assert branch_param.default is not inspect.Parameter.empty, "'branch' parameter in push should be optional (has default)."

    # Check pull
    assert hasattr(GM, 'pull')
    pull_sig = inspect.signature(GM.pull)
    assert 'branch' in pull_sig.parameters, "pull missing 'branch' parameter."
    branch_param = pull_sig.parameters['branch']
    assert branch_param.default is not inspect.Parameter.empty, "'branch' parameter in pull should be optional (has default)."