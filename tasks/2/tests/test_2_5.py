import os

def test_env_example():
    file_path = '.env.example'
    assert os.path.exists(file_path), ".env.example file does not exist"

    with open(file_path, 'r') as f:
        lines = f.readlines()

    var_count = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped and '=' in stripped and not stripped.startswith('#'):
            # Check preceding comment
            assert i > 0, "First line cannot be a variable without preceding comment"
            prev_stripped = lines[i-1].strip()
            assert prev_stripped.startswith('#'), f"No comment before variable at line {i+1}"
            # Check placeholder (empty value after =)
            key, value = stripped.split('=', 1)
            assert value.strip() == '', f"Variable '{key}' should have empty placeholder value"
            var_count += 1

    assert var_count >= 1, "At least one documented variable required"