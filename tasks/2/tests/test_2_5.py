import os

def test_env_example():
    file_path = '.env.example'
    assert os.path.exists(file_path), f"{file_path} does not exist in the project root."

    with open(file_path, 'r') as f:
        lines = f.readlines()

    var_lines = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped and not stripped.startswith('#'):
            parts = stripped.split('=', 1)
            if len(parts) != 2 or parts[1].strip() != '':
                assert False, f"Line {i+1}: '{line.strip()}' is not a proper placeholder (should be VAR= with empty value)"
            var_lines.append(i)

    assert len(var_lines) >= 1, "At least one environment variable required"

    for var_idx in var_lines:
        if var_idx == 0 or not lines[var_idx - 1].strip().startswith('#'):
            assert False, f"Environment variable at line {var_idx+1} is not preceded immediately by a comment."
