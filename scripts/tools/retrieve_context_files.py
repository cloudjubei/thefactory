import os
import json

def retrieve_context_files_tool(repo_path: str, paths: list) -> str:
    """
    Reads and returns the content of the files at the given paths.
    The result is a JSON string mapping file paths to their content.
    """
    retrieved_content = {}
    for path in paths:
        full_path = os.path.join(repo_path, path)
        if not _is_within_base(full_path, repo_path):
            retrieved_content[path] = f"Error: Path outside repository boundaries is not allowed: {path}"
            continue
        if not os.path.exists(full_path):
            retrieved_content[path] = f"Error: File not found at {path}"
            continue
        if not os.path.isfile(full_path):
            retrieved_content[path] = f"Error: Path is not a file: {path}"
            continue
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                retrieved_content[path] = f.read()
        except Exception as e:
            retrieved_content[path] = f"Error reading file {path}: {e}"
    return json.dumps(retrieved_content, indent=2)

def _is_within_base(path: str, base: str) -> bool:
    base_real = os.path.realpath(base)
    path_real = os.path.realpath(path)
    return os.path.commonpath([path_real, base_real]) == base_real
