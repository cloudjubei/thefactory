import os
import json

def retrieve_context_files_tool(repo_path: str, paths: list):
    content = {}
    for path in paths:
        full_path = os.path.join(repo_path, path)
        try:
            with open(full_path, "r") as f:
                content[path] = f.read()
        except FileNotFoundError:
            content[path] = f"Error: File '{path}' not found."
        except Exception as e:
            content[path] = f"Error reading file '{path}': {str(e)}"
    return json.dumps(content)
