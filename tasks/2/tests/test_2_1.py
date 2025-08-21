import importlib


def test_git_manager_exists_and_has_required_methods():
    module = importlib.import_module('scripts.git_manager')
    assert hasattr(module, 'GitManager'), 'GitManager class not found in scripts/git_manager.py'

    GitManager = getattr(module, 'GitManager')
    gm = GitManager(repo_url='https://example.com/repo.git', working_dir='/tmp/repo')
    assert gm is not None

    # Verify presence of commonly needed methods for git interactions
    required_methods = [
        'setup_repository',
        'ensure_user_config',
        'create_branch',
        'checkout_branch',
        'current_branch',
        'commit_all',
        'push_branch',
        'tag',
        'push_tags',
        'pull_rebase',
        'merge',
        'get_repo_url',
        'create_pull_request',
        'open_pull_request',  # alias
    ]

    missing = [m for m in required_methods if not hasattr(gm, m) or not callable(getattr(gm, m))]
    assert not missing, f"GitManager is missing required methods: {missing}"
