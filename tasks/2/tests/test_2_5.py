import os

def test_env_example():
    assert os.path.exists('.env.example'), 'File .env.example does not exist'
    with open('.env.example', 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    has_variable = False
    i = 0
    while i < len(lines):
        if lines[i] and not lines[i].startswith('#') and '=' in lines[i]:
            # Check if previous line exists and is a comment
            if i == 0 or not lines[i-1].startswith('#'):
                assert False, f'Variable at line {i+1} lacks a preceding comment'
            # Check if it's a placeholder (empty or no value after =)
            value = lines[i].split('=', 1)[1].strip()
            assert value == '', f'Variable at line {i+1} should be a placeholder (empty value)'
            has_variable = True
        i += 1
    assert has_variable, 'No environment variables found in .env.example'