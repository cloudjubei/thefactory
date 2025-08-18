import os


def write_file_tool(repo_path: str, path: str, content: str) -> str:
    """
    Safely write or overwrite a file within the repository.

    Args:
        repo_path: Absolute path to the cloned repository root.
        path: Relative path to the file to write.
        content: Full file content to write.

    Returns:
        A human-readable status string.
    """
    if not isinstance(path, str) or path.strip() == "":
        return "Error: Invalid path provided to write_file_tool."

    # Ensure the target path stays within the repository
    abs_path = os.path.abspath(os.path.join(repo_path, path))
    if not abs_path.startswith(os.path.abspath(repo_path) + os.sep):
        return "Error: Attempted to write outside the repository."

    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    with open(abs_path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Wrote file: {path} ({len(content)} bytes)"
