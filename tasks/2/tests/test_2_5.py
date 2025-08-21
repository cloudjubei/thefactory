import os
import re

def test_env_example():
    file_path = '.env.example'
    assert os.path.exists(file_path), 'File .env.example does not exist'
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    documented_vars = 0
    prev_line = None
    for line in lines:
        stripped = line.strip()
        if stripped == '' or stripped.startswith('#'):
            prev_line = stripped
            continue
        if '=' in stripped and not stripped.startswith('#'):
            assert prev_line is not None and prev_line.startswith('#'), f'Variable line "{line.strip()}" lacks a preceding comment'
            assert stripped.endswith('='), f'Placeholder "{stripped}" should be in the form VARIABLE='
            documented_vars += 1
            prev_line = stripped
        else:
            prev_line = stripped
    
    assert documented_vars >= 1, 'There should be at least one documented environment variable'