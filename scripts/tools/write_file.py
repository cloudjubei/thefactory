import os

def write_file_tool(repo_path: str, path: str, content: str):
    full_path = os.path.join(repo_path, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f: f.write(content)
    return f"Successfully wrote {len(content)} bytes to {path}"
