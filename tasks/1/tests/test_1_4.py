import os

def test_feature_1_4():
    file_path = 'docs/TESTING.md'
    assert os.path.exists(file_path), f"File {file_path} does not exist"
    with open(file_path, 'r') as f:
        content = f.read()
    required_headings = [
        '## Philosophy',
        '## Scope',
        '## Structure',
        '## Location',
        '## Naming Conventions',
        '## Tooling',
        '## Workflow'
    ]
    for heading in required_headings:
        assert heading in content, f"Heading '{heading}' not found in {file_path}"