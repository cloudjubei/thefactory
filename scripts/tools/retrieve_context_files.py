# scripts/tools/retrieve_context_files.py

from typing import List, Dict, Any
import os


def _safe_join(base_dir: str, relative_path: str) -> str:
    """
    Safely join base_dir with relative_path, preventing directory traversal.
    Returns the absolute normalized path.
    Raises ValueError if the resulting path escapes base_dir.
    """
    # Normalize and join
    norm_rel = os.path.normpath(relative_path).lstrip(os.sep)
    abs_path = os.path.abspath(os.path.join(base_dir, norm_rel))
    base_abs = os.path.abspath(base_dir)

    # Ensure the path is within the repo directory
    if not abs_path.startswith(base_abs + os.sep) and abs_path != base_abs:
        raise ValueError("Attempted to access path outside of repository")
    return abs_path


def retrieve_context_files_tool(base_dir: str, paths: List[str]) -> Dict[str, Any]:
    """
    Retrieve the contents of specified files within the repository.

    Args:
        base_dir: Absolute path to the repository root (provided by orchestrator).
        paths: List of relative file paths to retrieve.

    Returns:
        Dict with keys:
        - ok (bool): True if operation succeeded (even with some file errors), False only on invalid input.
        - files (list): List of {path, content} for successfully read files.
        - errors (list): List of {path, error} for files that couldn't be read.
    """
    result = {
        "ok": True,
        "files": [],
        "errors": []
    }

    if not isinstance(paths, list):
        return {"ok": False, "files": [], "errors": [{"path": "__input__", "error": "paths must be a list"}]}

    for p in paths:
        try:
            if not isinstance(p, str) or p.strip() == "":
                raise ValueError("path must be a non-empty string")
            abs_path = _safe_join(base_dir, p)
            if not os.path.exists(abs_path):
                result["errors"].append({"path": p, "error": "file does not exist"})
                continue
            if os.path.isdir(abs_path):
                result["errors"].append({"path": p, "error": "path is a directory"})
                continue
            # Read as UTF-8 text; replace undecodable bytes to avoid crashes
            with open(abs_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            result["files"].append({"path": p, "content": content})
        except Exception as e:
            result["errors"].append({"path": p if isinstance(p, str) else str(p), "error": str(e)})

    return result


__all__ = ["retrieve_context_files_tool"]
