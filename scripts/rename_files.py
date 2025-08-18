#!/usr/bin/env python3
"""
Safe rename/move operations within the repository.
Implements the rename_files tool described in docs/TOOL_ARCHITECTURE.md.

Function: rename_files(operations, overwrite=False, dry_run=False) -> str(JSON)
- operations: list of {"from_path": str, "to_path": str}
- overwrite: allow replacing existing destination
- dry_run: validate and report without making changes

Returns JSON string with keys:
- ok (bool)
- summary: {moved, skipped, errors}
- results: list of per-operation results: {status: "moved"|"skipped"|"error", message, from_path, to_path}

The tool validates paths so that no operation can escape the repository root.
"""
from __future__ import annotations
import json
import os
import shutil
from typing import List, Dict, Any


def _repo_root() -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    return os.path.abspath(os.path.join(here, ".."))


def _safe_path(p: str) -> str:
    root = _repo_root()
    abs_path = os.path.abspath(os.path.join(root, p))
    if not abs_path.startswith(root + os.sep) and abs_path != root:
        raise ValueError(f"Path escapes repository root: {p}")
    return abs_path


def rename_files(operations: List[Dict[str, str]], overwrite: bool = False, dry_run: bool = False) -> str:
    results: List[Dict[str, Any]] = []
    moved = skipped = errors = 0
    root = _repo_root()

    for op in operations:
        from_rel = op.get("from_path")
        to_rel = op.get("to_path")
        res: Dict[str, Any] = {
            "from_path": from_rel,
            "to_path": to_rel,
            "status": "",
            "message": ""
        }
        try:
            if not from_rel or not to_rel:
                raise ValueError("Both 'from_path' and 'to_path' are required")
            from_abs = _safe_path(from_rel)
            to_abs = _safe_path(to_rel)

            if not os.path.exists(from_abs):
                res["status"] = "error"
                res["message"] = "Source does not exist"
                errors += 1
                results.append(res)
                continue

            to_dir = os.path.dirname(to_abs)
            if to_dir and not os.path.exists(to_dir):
                if not dry_run:
                    os.makedirs(to_dir, exist_ok=True)

            if os.path.exists(to_abs):
                if not overwrite:
                    res["status"] = "skipped"
                    res["message"] = "Destination exists (overwrite=False)"
                    skipped += 1
                    results.append(res)
                    continue
                else:
                    if not dry_run:
                        # Remove destination (file or directory)
                        if os.path.isdir(to_abs) and not os.path.islink(to_abs):
                            shutil.rmtree(to_abs)
                        else:
                            os.remove(to_abs)

            if dry_run:
                res["status"] = "moved"
                res["message"] = "Dry run: validated"
                moved += 1
            else:
                shutil.move(from_abs, to_abs)
                res["status"] = "moved"
                res["message"] = "Moved successfully"
                moved += 1
        except Exception as e:
            res["status"] = "error"
            res["message"] = str(e)
            errors += 1
        results.append(res)

    ok = errors == 0
    summary = {"moved": moved, "skipped": skipped, "errors": errors}
    return json.dumps({"ok": ok, "summary": summary, "results": results}, indent=2)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Safely rename/move files within the repo root.")
    parser.add_argument("ops", help="Path to a JSON file with operations list: [{from_path, to_path}, ...]")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    with open(args.ops, "r", encoding="utf-8") as f:
        operations = json.load(f)

    print(rename_files(operations, overwrite=args.overwrite, dry_run=args.dry_run))
