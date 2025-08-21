import os
import re

def test_env_example():
    file_path = '.env.example'
    assert os.path.exists(file_path), "'.env.example' does not exist"
    
    with open(file_path, 'r') as f:
        lines = [line.rstrip() for line in f.readlines()]  # rstrip to handle trailing spaces
    
    variables = []
    for i, line in enumerate(lines):
        if re.match(r'^\w+=$', line.strip()):  # Check for VARIABLE=
            assert i > 0 and lines[i-1].strip().startswith('#'), f"Variable '{line.strip()}' lacks immediately preceding comment"
            variables.append(line.strip())
    
    assert len(variables) >= 1, "No documented environment variables found"
