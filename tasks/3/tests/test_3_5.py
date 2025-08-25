import re
from pathlib import Path

def test_feature_3_5():
    script_path = Path('scripts/child_project_utils.py')
    script_content = script_path.read_text(encoding='utf-8')

    # Expected template content from reference
    expected_template = """# File Organisation\n\nThis document describes how files and directories are organised in this repository to keep the project navigable, consistent, and easy to evolve.\n\n## Top-Level Directory Layout\n- src/: Source code for all tasks.\n- docs/: Project documentation and specifications.\n- tasks/: Per-task workspaces containing task metadata and tests.\n  - tasks/{id}/task.json: Canonical task definition for a single task.\n  - tasks/{id}/tests/: Deterministic tests validating each feature in the task.\n- .env, and other setup files may exist as needed.\n\nNotes:\n- All changes should be localized to the smallest reasonable scope (task- or doc-specific) to reduce coupling.\n- Documentation in docs/ is the single source of truth for specs and formats.\n\n## File Naming Conventions\n- Tasks and features:\n  - Task directories are numeric IDs: tasks/{id}/ (e.g., tasks/1/).\n  - Tests are named per-feature: tasks/{task_id}/tests/test_{task_id}_{feature_number}.py (e.g., tasks/15/tests/test_15_3.py).\n- Python modules: snake_case.py (e.g., task_format.py, run_local_agent.py).\n- Javascript modules: camelCase.js (e.g., taskFormat.js, runLocalAgent.js).\n- Documentation files: UPPERCASE or Title_Case for project-wide specs (e.g., TESTING.md, FILE_ORGANISATION.md). Place task-related docs under docs/tasks/.\n- JSON examples/templates: Use .json with clear, descriptive names (e.g., task_example.json).\n\n## Evolution Guidance\n- Make minimal, incremental changes that are easy to review and test.\n- Keep documentation authoritative: update docs first when changing schemas or protocols.\n- Introduce shared utilities only when multiple tasks need them; otherwise keep helpers local to a task.\n- Deprecate gradually: create new files/specs alongside old ones, migrate, then remove deprecated artifacts when tests prove stability.\n- Each feature must have deterministic tests; do not mark features complete until tests pass.\n\n## Example Tree (illustrative)\nThe following tree is graphical and illustrative of a typical repository layout:\n\n```\nrepo_root/\n├─ .env\n├─ .gitignore\n├─ src/\n├─ docs/\n│  ├─ FILE_ORGANISATION.md\n└─ tasks/\n   ├─ 1/\n   │  ├─ task.json\n   │  └─ tests/\n   │     └─ test_1_3.py\n   └─ 2/\n      ├─ task.json\n      └─ tests/\n```\n\nThis diagram shows how documentation, scripts, and per-task artifacts are arranged, including where tests for each feature live and how the main code structure is organized. \n"""

    # Check for template constant
    assert 'CHILD_FILE_ORGANISATION_TEMPLATE = """' in script_content, 'Template constant missing'
    assert expected_template in script_content, 'Template content does not match reference'

    # Check for directory creations
    assert re.search(r"\(project_path / 'src'\)\.mkdir\(\)\s*", script_content), 'src directory creation missing'
    assert re.search(r"\(project_path / 'docs'\)\.mkdir\(\)\s*", script_content), 'docs directory creation missing'
    assert re.search(r"\(project_path / 'docs' / 'FILE_ORGANISATION.md'\)\.write_text\(CHILD_FILE_ORGANISATION_TEMPLATE, encoding='utf-8'\)", script_content), 'FILE_ORGANISATION.md write missing'

    # Check plan_actions
    assert "'Create directory: src'" in script_content, 'plan_actions for src missing'
    assert "'Create directory: docs'" in script_content, 'plan_actions for docs missing'
    assert "'Create file: docs/FILE_ORGANISATION.md'" in script_content, 'plan_actions for file missing'

    # Check parent's FILE_ORGANISATION.md
    parent_path = Path('docs/FILE_ORGANISATION.md')
    parent_content = parent_path.read_text(encoding='utf-8')
    assert '## Child Project Structure' in parent_content, 'Child Project Structure section missing'
    assert 'src/' in parent_content and 'docs/' in parent_content and 'tasks/' in parent_content, 'Key directories not described in parent doc'
    assert 'example tree' in parent_content.lower() and 'child project' in parent_content.lower(), 'Child project example tree missing'

test_feature_3_5()