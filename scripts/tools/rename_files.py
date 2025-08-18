import os
import shutil
from typing import List, Dict


def _within_repo(base_dir: str, target_path: str) -> bool:
    base_abs = os.path.abspath(base_dir)
    target_abs = os.path.abspath(target_path)
    return target_abs.startswith(base_abs + os.sep)


def rename_files(operations: List[Dict], base_dir: str, overwrite: bool = False, dry_run: bool = False) -> Dict:
    """
    Safely rename or move files/directories within the repository.

    Args:
        operations: List of {"from_path": str, "to_path": str}
        base_dir: Repository root (absolute path) where operations occur
        overwrite: Allow overwriting existing destination files
        dry_run: If True, only validate and report, do not make changes

    Returns:
        Dict with keys: ok (bool), summary (dict), results (list)
    """
    results = []
    moved = 0
    skipped = 0
    errors = 0

    if not isinstance(operations, list):
        return {"ok": False, "summary": {"moved": 0, "skipped": 0, "errors": 1}, "results": [{"status": "error", "message": "operations must be a list"}]}

    for op in operations:
        from_rel = op.get("from_path")
        to_rel = op.get("to_path")
        if not from_rel or not to_rel:
            results.append({"status": "error", "message": "Missing from_path or to_path"})
            errors += 1
            continue

        src = os.path.abspath(os.path.join(base_dir, from_rel))
        dst = os.path.abspath(os.path.join(base_dir, to_rel))

        if not _within_repo(base_dir, src) or not _within_repo(base_dir, dst):
            results.append({"status": "error", "message": f"Path escapes repository root: {from_rel} -> {to_rel}"})
            errors += 1
            continue

        if not os.path.exists(src):
            results.append({"status": "error", "message": f"Source does not exist: {from_rel}"})
            errors += 1
            continue

        if os.path.exists(dst) and not overwrite:
            results.append({"status": "skipped", "message": f"Destination exists and overwrite=False: {to_rel}"})
            skipped += 1
            continue

        if dry_run:
            results.append({"status": "dry_run", "message": f"Would move {from_rel} -> {to_rel}"})
            continue

        try:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.move(src, dst)
            results.append({"status": "moved", "message": f"Moved {from_rel} -> {to_rel}"})
            moved += 1
        except Exception as e:
            results.append({"status": "error", "message": f"Failed to move {from_rel} -> {to_rel}: {e}"})
            errors += 1

    ok = errors == 0
    summary = {"moved": moved, "skipped": skipped, "errors": errors}
    return {"ok": ok, "summary": summary, "results": results}
