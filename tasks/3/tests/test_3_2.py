import os
import re
from pathlib import Path

def check_criteria():
    failures = []
    guide_path = Path('docs') / 'PROJECTS_GUIDE.md'
    if not guide_path.is_file():
        failures.append('Criterion 1 failed: docs/PROJECTS_GUIDE.md does not exist.')
    else:
        with open(guide_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'child_project_utils.py' not in content:
            failures.append('Criterion 2 failed: No mention of child_project_utils.py in the documentation.')
        heading_pattern = re.compile(r'^#{1,3}\s+.*(script|child_project_utils|creating\s+new\s+child\s+project)', re.IGNORECASE | re.MULTILINE)
        if not heading_pattern.search(content):
            failures.append('Criterion 3 failed: No relevant heading for script usage.')
        list_pattern = re.compile(r'(\n\s*([0-9]+\.|-|\*)\s+.+){3,}', re.MULTILINE)
        if not list_pattern.search(content):
            failures.append('Criterion 4 failed: No step-by-step list with at least 3 steps found.')
        if 'python3 scripts/child_project_utils.py' not in content:
            failures.append('Criterion 5 failed: No example script invocation found.')
        required_terms = ['git submodule add', 'git submodule update --remote', 'git submodule deinit']
        for term in required_terms:
            if term not in content:
                failures.append(f'Criterion 6 failed: Missing term "{term}" in submodules guide.')
    if failures:
        print('Some criteria failed:')
        for fail in failures:
            print(fail)
    else:
        print('All acceptance criteria passed.')

if __name__ == '__main__':
    check_criteria()
