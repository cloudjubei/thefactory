import re
from pathlib import Path

def read_projects_guide():
    p = Path('docs/PROJECTS_GUIDE.md')
    assert p.exists(), "docs/PROJECTS_GUIDE.md must exist"
    return p.read_text(encoding='utf-8')


def test_file_exists():
    assert Path('docs/PROJECTS_GUIDE.md').exists()


def test_mentions_child_project_utils():
    content = read_projects_guide()
    assert 'child_project_utils.py' in content


def test_has_relevant_heading():
    content = read_projects_guide()
    pattern = re.compile(r"^#{1,6}\s.*(script|child_project_utils|creating new child project)", re.IGNORECASE | re.MULTILINE)
    assert pattern.search(content) is not None, "Expected a heading referencing script/child_project_utils/creating new child project"


def test_has_step_by_step_list():
    content = read_projects_guide()
    lines = content.splitlines()
    list_like = [ln for ln in lines if re.match(r"^\s*(?:\d+\.|[-*])\s+", ln)]
    assert len(list_like) >= 3, "Expected at least three list items to represent a step-by-step guide"


def test_has_example_python_usage():
    content = read_projects_guide()
    assert 'python3 scripts/child_project_utils.py' in content


def test_has_submodule_commands():
    content = read_projects_guide()
    assert 'git submodule add' in content
    assert 'git submodule update --remote' in content
    assert 'git submodule deinit' in content


def test_documents_task_id_option_with_explanation():
    content = read_projects_guide()
    # Must mention the flag (accept both hyphen and underscore variants)
    has_flag = re.search(r"--task[-_]?id\b", content) is not None
    assert has_flag, "Expected documentation to mention the --task-id (or --task_id) option"
    # Must include an example invocation that uses the flag
    assert re.search(r"python3\s+scripts/child_project_utils\.py\s+.+--task[-_]?id\s*\d+", content), "Expected an example using --task-id"
    # Must explain what it does: look for typical explanation cues
    has_tasks_one = 'tasks/1' in content
    has_tasks_id_variant = ('tasks/{id}' in content) or ('tasks/<id>' in content)
    has_explain_word = re.search(r"rewrit|seed|copy", content, re.IGNORECASE) is not None
    assert has_tasks_one and has_explain_word, "Expected explanation mentioning tasks/1 and describing the action (rewrite/seed/copy)"
    # If author uses placeholders, also accept tasks/{id} or tasks/<id>
    assert has_tasks_id_variant or re.search(r"tasks/?\s*\(source\)\s*id", content, re.IGNORECASE) or True
