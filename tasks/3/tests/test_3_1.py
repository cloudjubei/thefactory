import os
import re

def check_file_exists(path):
    return os.path.exists(path)

def read_file_content(path):
    with open(path, 'r') as f:
        return f.read()

def has_section(content, section_name):
    return re.search(r'^#*\s*' + re.escape(section_name) + r'\s*$', content, re.MULTILINE | re.IGNORECASE) is not None

def contains_phrase(content, phrase):
    return phrase.lower() in content.lower()

def test_all_criteria():
    assert check_file_exists('docs/PROJECTS_GUIDE.md'), 'Criterion 1 failed'
    guide_content = read_file_content('docs/PROJECTS_GUIDE.md')
    assert check_file_exists('docs/FILE_ORGANISATION.md'), 'FILE_ORGANISATION.md missing'
    org_content = read_file_content('docs/FILE_ORGANISATION.md')
    assert 'PROJECTS_GUIDE.md' in org_content, 'Criterion 2 failed'
    assert has_section(guide_content, 'Overview'), 'Criterion 3 failed: no Overview section'
    assert contains_phrase(guide_content, 'purpose of the projects/ folder') and contains_phrase(guide_content, 'each child project is a git submodule'), 'Criterion 3 failed: missing explanations'
    assert contains_phrase(guide_content, 'git clone --recurse-submodules') and contains_phrase(guide_content, 'git submodule init') and contains_phrase(guide_content, 'git submodule update') and contains_phrase(guide_content, 'git submodule update --init --recursive'), 'Criterion 4 failed'
    assert contains_phrase(guide_content, 'git submodule add -b') and contains_phrase(guide_content, 'projects/<name>') and contains_phrase(guide_content, 'commit both .gitmodules and'), 'Criterion 5 failed'
    assert contains_phrase(guide_content, 'git submodule update --remote') and contains_phrase(guide_content, 'entering the submodule and pulling') and contains_phrase(guide_content, 'committing the pointer bump') and contains_phrase(guide_content, 'git submodule foreach'), 'Criterion 6 failed'
    assert contains_phrase(guide_content, 'git config -f .gitmodules submodule.projects/<name>.branch') and contains_phrase(guide_content, 'committing .gitmodules'), 'Criterion 7 failed'
    assert contains_phrase(guide_content, 'git submodule deinit -f projects/<name>') and contains_phrase(guide_content, 'git rm -f projects/<name>') and contains_phrase(guide_content, 'rm -rf .git/modules/projects/<name>') and contains_phrase(guide_content, '.gitmodules is updated and committed'), 'Criterion 8 failed'
    assert has_section(guide_content, 'Common pitfalls') and contains_phrase(guide_content, 'detached HEAD in submodules') and contains_phrase(guide_content, 'uncommitted changes in submodules') and contains_phrase(guide_content, 'mixing SSH and HTTPS URLs') and contains_phrase(guide_content, 'forgetting to commit .gitmodules') and contains_phrase(guide_content, 'not committing the submodule pointer update') and contains_phrase(guide_content, 'needing git submodule sync') and contains_phrase(guide_content, 'ensuring CI uses --init --recursive'), 'Criterion 9 failed'
    assert has_section(guide_content, 'CI/CD notes') and contains_phrase(guide_content, 'git clone --recurse-submodules') and contains_phrase(guide_content, 'git submodule update --init --recursive'), 'Criterion 10 failed'
    assert has_section(guide_content, 'Troubleshooting') and contains_phrase(guide_content, 'git submodule sync') and contains_phrase(guide_content, 'git submodule status'), 'Criterion 11 failed'
    assert (has_section(guide_content, 'Quick reference') or has_section(guide_content, 'cheat sheet')) and contains_phrase(guide_content, 'clone/init') and contains_phrase(guide_content, 'add') and contains_phrase(guide_content, 'update') and contains_phrase(guide_content, 'switch branch') and contains_phrase(guide_content, 'remove') and contains_phrase(guide_content, 'status'), 'Criterion 12 failed'
    assert contains_phrase(guide_content, 'projects/<name>') and contains_phrase(guide_content, 'changes inside a submodule should be committed within the submodule') and contains_phrase(guide_content, 'superproject pointer updated and committed'), 'Criterion 13 failed'
    commands = ['git clone --recurse-submodules', 'git submodule init', 'git submodule update', 'git submodule update --init --recursive', 'git submodule add -b', 'git submodule update --remote', 'git submodule foreach', 'git submodule status', 'git config -f .gitmodules submodule.projects/<name>.branch <branch>', 'git submodule deinit -f', 'git rm -f projects/<name>', 'rm -rf .git/modules/projects/<name>', 'git submodule sync']
    for cmd in commands:
        assert contains_phrase(guide_content, cmd), f'Criterion 14 failed: missing {cmd}'
    assert contains_phrase(guide_content, 'authentication schemes (SSH vs HTTPS)') and contains_phrase(guide_content, 'warns about mixing them'), 'Criterion 15 failed'
    print('All criteria passed')

test_all_criteria()