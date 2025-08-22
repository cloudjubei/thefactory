import json
import os
from pathlib import Path
import pytest

"""
Acceptance test for Feature 3.5: Script: Post-migration validation and cleanup

Expected public API (to be implemented by development):

Module: child_projects.post_migration
Function: validate_and_cleanup(repo, apply=False, expected_counts=None, report_dir=None, fail_on="errors", policy=None, now=None) -> dict

- repo: a repository/DAO-like object used by the function to interact with persistence; tests provide a fake implementation.
- apply: when False (default), perform a dry-run (no mutations). When True, perform cleanup actions transactionally.
- expected_counts: a mapping of parent_id -> expected active child count; used for reconciliation.
- report_dir: directory to write JSON and Markdown report files and a log file.
- fail_on: one of {"errors", "warnings", "never"} controlling exit_code behavior.
- policy: optional dict to specify duplicate remediation policy, e.g., {"duplicates": "delete" or "archive"}.
- now: optional time injection for deterministic timestamps.

Return value (dict) must include keys:
- status: one of {"ok", "warnings", "errors"}
- exit_code: integer per acceptance criteria
- summary: dict with counts (at least: total_parents, total_children, errors_count, warnings_count)
- issues: dict containing lists/details for categories like orphans, duplicates, count_mismatches
- actions: dict with "planned" (list of actions) and "executed" (list of actions)
- report_files: dict with paths for {"json", "markdown", "log"}

The function should not require a real database; it should operate via the provided repo interface. A separate CLI may wrap this function; CLI testing is out of scope here.
"""

class FakeRepo:
    """A simple in-memory repo to simulate parents/children and transactional behavior."""
    def __init__(self):
        # Parents: 1 exists, 2 exists; 999 does not.
        self.parents = {
            1: {"id": 1, "name": "Parent A"},
            2: {"id": 2, "name": "Parent B"},
        }
        # Children: include valid, duplicate, orphan, archived
        self.children = {
            10: {"id": 10, "parent_id": 1, "code": "C1", "legacy_id": "L1", "archived": False, "created_at": 1},
            11: {"id": 11, "parent_id": 1, "code": "C2", "legacy_id": "L2", "archived": False, "created_at": 2},
            12: {"id": 12, "parent_id": 1, "code": "C2", "legacy_id": "L2", "archived": False, "created_at": 3},  # duplicate
            13: {"id": 13, "parent_id": 999, "code": "C3", "legacy_id": "L3", "archived": False, "created_at": 4},  # orphan
            14: {"id": 14, "parent_id": 1, "code": "C4", "legacy_id": "L4", "archived": True,  "created_at": 5},  # archived
        }
        self.deleted = set()
        self.archived = set()
        self._in_txn = False
        self._txn_log = []
        self.fail_during_apply = False

    # Data access methods expected by implementation
    def list_parents(self):
        return list(self.parents.values())

    def list_children(self):
        return list(self.children.values())

    def begin(self):
        repo = self
        class Txn:
            def __enter__(self_non):
                repo._in_txn = True
                repo._txn_log = []
                return repo
            def __exit__(self_non, exc_type, exc, tb):
                # Roll back on exception
                if exc:
                    for op, child_id, prev in reversed(repo._txn_log):
                        if op == "delete":
                            # Undo delete
                            repo.children[child_id] = prev
                            repo.deleted.discard(child_id)
                        elif op == "archive":
                            # Undo archive flag
                            repo.children[child_id]["archived"] = prev
                            repo.archived.discard(child_id)
                    repo._in_txn = False
                    repo._txn_log = []
                    # Propagate exception
                    return False
                # Commit: simply clear the txn log
                repo._in_txn = False
                repo._txn_log = []
                return False
        return Txn()

    def delete_child(self, child_id: int):
        prev = self.children.get(child_id)
        if prev is None:
            return
        del self.children[child_id]
        self.deleted.add(child_id)
        if self._in_txn:
            self._txn_log.append(("delete", child_id, prev))
        # Inject a failure at a specific point to test rollback behavior
        if self.fail_during_apply and child_id == 12:
            raise RuntimeError("Injected failure during delete")

    def archive_child(self, child_id: int):
        if child_id not in self.children:
            return
        prev_archived = self.children[child_id]["archived"]
        self.children[child_id]["archived"] = True
        self.archived.add(child_id)
        if self._in_txn:
            self._txn_log.append(("archive", child_id, prev_archived))


@pytest.fixture()
def expected_counts():
    # Expected active (non-archived) children counts per parent after cleanup
    # Parent 1 should have 2 active children (C1, C2). Parent 2 has 0.
    return {1: 2, 2: 0}


def _import_target():
    mod = pytest.importorskip(
        "child_projects.post_migration",
        reason="Implementation module child_projects.post_migration not found yet."
    )
    func = getattr(mod, "validate_and_cleanup", None)
    if func is None:
        pytest.skip("validate_and_cleanup(repo, ...) is not implemented yet")
    return func


def test_dry_run_reports_issues_without_mutation(tmp_path: Path, expected_counts):
    validate_and_cleanup = _import_target()
    repo = FakeRepo()

    # Snapshot initial state
    initial_ids = set(repo.children.keys())

    result = validate_and_cleanup(
        repo=repo,
        apply=False,
        expected_counts=expected_counts,
        report_dir=tmp_path,
        fail_on="errors",
        policy={"duplicates": "delete"},
    )

    # Basic shape assertions
    assert isinstance(result, dict)
    assert result.get("status") in {"errors", "warnings", "ok"}
    # With duplicates and orphans present, status should reflect issues; most likely "errors"
    assert result.get("status") in {"errors", "warnings"}
    assert isinstance(result.get("exit_code"), int)
    actions = result.get("actions", {})
    planned = actions.get("planned", [])
    executed = actions.get("executed", [])
    assert isinstance(planned, list)
    assert isinstance(executed, list)
    # Dry run must not execute actions
    assert len(executed) == 0
    # There should be at least some planned actions (duplicates/orphans)
    assert len(planned) >= 1

    # State must be unchanged
    assert set(repo.children.keys()) == initial_ids

    # Report files must exist and be well-formed
    report_files = result.get("report_files", {})
    json_path = Path(report_files.get("json", ""))
    md_path = Path(report_files.get("markdown", ""))
    log_path = Path(report_files.get("log", ""))
    assert json_path.is_file(), f"JSON report not found at {json_path}"
    assert md_path.is_file(), f"Markdown report not found at {md_path}"
    assert log_path.is_file(), f"Log file not found at {log_path}"

    with open(json_path, "r", encoding="utf-8") as f:
        payload = json.load(f)
    assert "summary" in payload and isinstance(payload["summary"], dict)
    assert "issues" in payload and isinstance(payload["issues"], dict)
    assert "actions" in payload and isinstance(payload["actions"], dict)


def test_apply_cleans_issues_transactional_and_idempotent(tmp_path: Path, expected_counts):
    validate_and_cleanup = _import_target()

    # Successful apply
    repo = FakeRepo()
    res_apply = validate_and_cleanup(
        repo=repo,
        apply=True,
        expected_counts=expected_counts,
        report_dir=tmp_path,
        fail_on="errors",
        policy={"duplicates": "delete"},
    )

    # After cleanup: duplicate id=12 and orphan id=13 should be gone
    remaining_ids = set(repo.children.keys())
    assert 12 not in remaining_ids, "Duplicate child was not removed during apply"
    assert 13 not in remaining_ids, "Orphan child was not removed during apply"
    assert {10, 11, 14}.issubset(remaining_ids), "Valid/archived children should remain"

    # Executed actions should be non-empty
    executed = res_apply.get("actions", {}).get("executed", [])
    assert len(executed) >= 1

    # Status and exit code should indicate success after cleanup
    assert res_apply.get("status") in {"ok", "warnings"}
    # With counts matching expected and no remaining errors, exit_code should be 0
    assert res_apply.get("exit_code") == 0

    # Idempotency: running again should yield zero planned/executed actions
    res_again = validate_and_cleanup(
        repo=repo,
        apply=True,
        expected_counts=expected_counts,
        report_dir=tmp_path,
        fail_on="errors",
        policy={"duplicates": "delete"},
    )
    assert res_again.get("exit_code") == 0
    assert res_again.get("status") in {"ok", "warnings"}
    assert len(res_again.get("actions", {}).get("planned", [])) == 0
    assert len(res_again.get("actions", {}).get("executed", [])) == 0

    # Transaction rollback on failure
    repo_fail = FakeRepo()
    repo_fail.fail_during_apply = True
    before_ids = set(repo_fail.children.keys())
    try:
        res_fail = validate_and_cleanup(
            repo=repo_fail,
            apply=True,
            expected_counts=expected_counts,
            report_dir=tmp_path,
            fail_on="errors",
            policy={"duplicates": "delete"},
        )
    except Exception:
        # On exception, state must be rolled back to original
        after_ids = set(repo_fail.children.keys())
        assert after_ids == before_ids, "Repository state changed despite transactional failure"
    else:
        # If handled gracefully, expect non-zero exit and rolled-back state
        assert res_fail.get("exit_code", 1) != 0
        after_ids = set(repo_fail.children.keys())
        assert after_ids == before_ids, "Repository state changed despite transactional failure"
        # Report should indicate errors
        assert res_fail.get("status") == "errors"
        # Log file should exist
        log_path = Path(res_fail.get("report_files", {}).get("log", ""))
        assert log_path.is_file()


def test_fail_on_policy_controls_exit_code(tmp_path: Path, expected_counts):
    validate_and_cleanup = _import_target()
    repo = FakeRepo()

    # Use dry-run so issues remain, but fail_on=never should still exit 0
    res = validate_and_cleanup(
        repo=repo,
        apply=False,
        expected_counts=expected_counts,
        report_dir=tmp_path,
        fail_on="never",
        policy={"duplicates": "delete"},
    )
    assert isinstance(res.get("exit_code"), int)
    assert res.get("exit_code") == 0, "fail_on=never should produce exit_code 0 even with issues present"
