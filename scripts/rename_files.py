# scripts/rename_files.py

"""
rename_files tool

Provides a safe utility to rename/move files or directories within the repository.
This module is intended to be invoked by the AgentTools.rename_files method in
scripts/run_local_agent.py so the LLM can perform repository file organization steps.

All operations are restricted to the provided base_dir to prevent accidental modifications
outside the repository.

Usage:
    from rename_files import rename_files
    result = rename_files(
        operations=[{"from_path": "old/name.txt", "to_path": "new/name.txt"}],
        base_dir="/path/to/repo",
        overwrite=False,
        dry_run=False,
    )

Return value:
    A dict with keys:
      - ok (bool): True if all operations succeeded, else False
      - summary (dict): counts of moved, skipped, errors
      - results (list): per-operation result entries

Each result entry:
    {
      "from_path": str,
      "to_path": str,
      "status": "moved" | "skipped" | "error",
      "message": str
    }
"""

import os
import shutil
from typing import List, Dict, Any


def _is_within_base(path: str, base: str) -> bool:
    base_real = os.path.realpath(base)
    path_real = os.path.realpath(path)
    return os.path.commonpath([path_real, base_real]) == base_real


def rename_files(operations: List[Dict[str, Any]], base_dir: str, overwrite: bool = False, dry_run: bool = False) -> Dict[str, Any]:
    if not isinstance(operations, list):
        raise ValueError("operations must be a list of {from_path, to_path} objects")

    summary = {"moved": 0, "skipped": 0, "errors": 0}
    results = []

    for op in operations:
        from_rel = op.get("from_path")
        to_rel = op.get("to_path")

        if not isinstance(from_rel, str) or not isinstance(to_rel, str):
            results.append({
                "from_path": from_rel,
                "to_path": to_rel,
                "status": "error",
                "message": "from_path and to_path must be strings"
            })
            summary["errors"] += 1
            continue

        # Normalize paths and join with base_dir
        from_rel_norm = os.path.normpath(from_rel)
        to_rel_norm = os.path.normpath(to_rel)

        src = os.path.join(base_dir, from_rel_norm)
        dst = os.path.join(base_dir, to_rel_norm)

        # Safety: ensure both src and dst are within base_dir
        if not _is_within_base(src, base_dir) or not _is_within_base(dst, base_dir):
            results.append({
                "from_path": from_rel,
                "to_path": to_rel,
                "status": "error",
                "message": "Operation outside repository boundaries is not allowed"
            })
            summary["errors"] += 1
            continue

        if from_rel_norm == to_rel_norm:
            results.append({
                "from_path": from_rel,
                "to_path": to_rel,
                "status": "skipped",
                "message": "Source and destination are identical"
            })
            summary["skipped"] += 1
            continue

        if not os.path.exists(src):
            results.append({
                "from_path": from_rel,
                "to_path": to_rel,
                "status": "error",
                "message": "Source path does not exist"
            })
            summary["errors"] += 1
            continue

        if os.path.exists(dst) and not overwrite:
            results.append({
                "from_path": from_rel,
                "to_path": to_rel,
                "status": "error",
                "message": "Destination already exists (set overwrite=True to replace)"
            })
            summary["errors"] += 1
            continue

        if dry_run:
            results.append({
                "from_path": from_rel,
                "to_path": to_rel,
                "status": "skipped",
                "message": "Dry run: no changes made"
            })
            summary["skipped"] += 1
            continue

        # Ensure destination directory exists
        os.makedirs(os.path.dirname(dst), exist_ok=True)

        try:
            # shutil.move handles files and directories and cross-filesystem moves
            if os.path.exists(dst) and overwrite:
                # Remove destination before moving if overwrite requested
                if os.path.isdir(dst):
                    shutil.rmtree(dst)
                else:
                    os.remove(dst)
            shutil.move(src, dst)
            results.append({
                "from_path": from_rel,
                "to_path": to_rel,
                "status": "moved",
                "message": "Move completed"
            })
            summary["moved"] += 1
        except Exception as e:
            results.append({
                "from_path": from_rel,
                "to_path": to_rel,
                "status": "error",
                "message": f"Failed to move: {e}"
            })
            summary["errors"] += 1

    ok = summary["errors"] == 0
    return {"ok": ok, "summary": summary, "results": results}
