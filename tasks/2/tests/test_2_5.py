import os
import re
def test_env_example():
    file_path = '.env.example'
    assert os.path.exists(file_path), f"{file_path} does not exist in the project root."
    with open(file_path, 'r') as f:
        lines = f.readlines()
    documented_vars = 0
    for i in range(len(lines)):
        line = lines[i].strip()
        if re.match(r'^[A-Z_][A-Z0-9_]*=$', line):
            assert i > 0, "Placeholder at the beginning without comment."
            prev_line = lines[i-1].strip()
            assert prev_line.startswith('#'), f"Placeholder '{line}' at line {i+1} is not preceded by a comment."
            documented_vars += 1
    assert documented_vars >= 1, "No documented placeholders found in .env.example."