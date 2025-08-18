import os
import json
from typing import List, Dict, Any

def retrieve_context_files_tool(base_dir: str, paths: List[str]) -> str:
    """
    Safely read and return the content of the files at the given relative paths.

    Args:
        base_dir (str): The repository root directory.
        paths (List[str]): Relative file paths to retrieve.

    Returns:
        str: A JSON string with keys:
            ok (bool): Whether the operation succeeded overall
            results (list): List of per-file results with keys:
                path (str): The relative path requested
                ok (bool): Whether this file was read successfully
                content (str, optional): File content when ok is True
                error (str, optional): Error message when ok is False
    """
    results: List[Dict[str, Any]] = []

    abs_base = os.path.abspath(base_dir)

    for rel_path in paths:
        result: Dict[str, Any] = {"path": rel_path}
        try:
            # Normalize and prevent path traversal outside repo
            abs_path = os.path.abspath(os.path.join(base_dir, rel_path))
            if not abs_path.startswith(abs_base + os.sep) and abs_path != abs_base:
                result.update({"ok": False, "error": "Path escapes repository root"})
                results.append(result)
                continue

            if not os.path.exists(abs_path):
                result.update({"ok": False, "error": "File not found"})
                results.append(result)
                continue

            if os.path.isdir(abs_path):
                result.update({"ok": False, "error": "Path is a directory, not a file"})
                results.append(result)
                continue

            with open(abs_path, "r", encoding="utf-8") as f:
                content = f.read()
            result.update({"ok": True, "content": content})
            results.append(result)
        except Exception as e:
            result.update({"ok": False, "error": str(e)})
            results.append(result)

    return json.dumps({"ok": True, "results": results})
