import os
import json
from typing import List, Dict


def retrieve_context_files_tool(repo_path: str, paths: List[str]) -> str:
    """
    Retrieve and return the content of the files at the given relative paths.

    Args:
        repo_path: Absolute path to the cloned repository root.
        paths: List of relative file paths to read.

    Returns:
        JSON string with structure:
        {
          "ok": bool,
          "files": { "path": "content", ... },
          "missing": ["path", ...],
          "errors": ["message", ...]
        }
    """
    result: Dict[str, object] = {"ok": True, "files": {}, "missing": [], "errors": []}

    if not isinstance(paths, list):
        result["ok"] = False
        result["errors"].append("Invalid argument: 'paths' must be a list of strings.")
        return json.dumps(result)

    base_abs = os.path.abspath(repo_path)

    for rel in paths:
        try:
            if not isinstance(rel, str) or rel.strip() == "":
                result["errors"].append("Encountered an empty or non-string path.")
                result["ok"] = False
                continue
            abs_path = os.path.abspath(os.path.join(base_abs, rel))
            if not abs_path.startswith(base_abs + os.sep):
                result["errors"].append(f"Path escapes repository root: {rel}")
                result["ok"] = False
                continue
            if not os.path.exists(abs_path):
                result["missing"].append(rel)
                continue
            if os.path.isdir(abs_path):
                result["errors"].append(f"Path is a directory, not a file: {rel}")
                result["ok"] = False
                continue
            with open(abs_path, "r", encoding="utf-8") as f:
                result["files"][rel] = f.read()
        except Exception as e:
            result["errors"].append(f"Failed to read {rel}: {e}")
            result["ok"] = False

    return json.dumps(result)
