import json
import sqlite3
import subprocess
import sys
from pathlib import Path

# End-to-end test for the child projects structure generation script.
# Assumptions/specs under test (acceptance):
# - Executable via: python -m child_projects_structure
# - Supports flags: --config, --backend, --dsn, --dry-run, --metrics-out, --log-level
# - Supports sqlite backend
# - Creates entities, relationships (via join table), and indexes per config
# - Idempotent and supports dry-run
# - Writes metrics JSON with required schema


def _run_cli(args, cwd=None):
    """Run the CLI and return CompletedProcess."""
    cmd = [sys.executable, "-m", "child_projects_structure"] + args
    return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)


def _read_metrics(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _sqlite_objects(dsn: Path):
    """Return sets of table and index names in the sqlite DB."""
    con = sqlite3.connect(str(dsn))
    try:
        cur = con.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row[0] for row in cur.fetchall()}
        cur.execute("SELECT name FROM sqlite_master WHERE type='index'")
        indexes = {row[0] for row in cur.fetchall()}
        return tables, indexes
    finally:
        con.close()


def test_child_projects_structure_generation_idempotent_and_dry_run(tmp_path: Path):
    # Prepare sqlite database path and config
    db_path = tmp_path / "child_projects.db"
    config_path = tmp_path / "config.json"

    # Minimal JSON config for an entity 'task' with a many-to-many self-relationship and an index.
    config = {
        "version": 1,
        "entities": [
            {
                "name": "task",
                "columns": [
                    {"name": "id", "type": "integer", "primary_key": True},
                    {"name": "name", "type": "text", "unique": True},
                    {"name": "created_at", "type": "timestamp", "nullable": False}
                ],
                "indexes": [
                    {"name": "idx_task_name", "columns": ["name"], "unique": True}
                ]
            }
        ],
        "relationships": [
            {
                "name": "task_depends_on_task",
                "type": "many_to_many",
                "from": {"entity": "task", "column": "id"},
                "to": {"entity": "task", "column": "id"},
                "via": {
                    "table": "task_dependencies",
                    "from_column": "task_id",
                    "to_column": "depends_on_id",
                    "unique": True
                }
            }
        ]
    }

    config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")

    # 1) Dry-run: plan only, no schema changes
    metrics_dry = tmp_path / "metrics_dry.json"
    res = _run_cli([
        "--config", str(config_path),
        "--backend", "sqlite",
        "--dsn", str(db_path),
        "--dry-run",
        "--metrics-out", str(metrics_dry),
        "--log-level", "DEBUG",
    ])
    assert res.returncode == 0, f"Dry-run failed:\nSTDOUT:\n{res.stdout}\nSTDERR:\n{res.stderr}"
    assert metrics_dry.exists(), "Dry-run metrics file was not created"

    metrics = _read_metrics(metrics_dry)
    # Required metrics schema
    assert metrics.get("backend") == "sqlite"
    assert metrics.get("dry_run") is True
    assert isinstance(metrics.get("duration_ms"), (int, float))
    assert isinstance(metrics.get("config_hash"), str) and len(metrics["config_hash"]) >= 32
    counts = metrics.get("counts")
    assert isinstance(counts, dict), "counts must be present in metrics"
    for key in ("entities", "relationships", "indexes"):
        assert key in counts, f"counts.{key} missing"
        for ckey in ("planned", "created", "updated", "skipped"):
            assert ckey in counts[key], f"counts.{key}.{ckey} missing"
    # Planned counts should reflect 1 entity, 1 relationship, 1 index; created is zero in dry-run
    assert counts["entities"]["planned"] >= 1
    assert counts["relationships"]["planned"] >= 1
    assert counts["indexes"]["planned"] >= 1
    assert counts["entities"]["created"] == 0
    assert counts["relationships"]["created"] == 0
    assert counts["indexes"]["created"] == 0

    # Verify the database has not been modified in dry-run
    tables, indexes = _sqlite_objects(db_path)
    assert "task" not in tables
    assert "task_dependencies" not in tables
    assert "idx_task_name" not in indexes

    # 2) Apply: perform actual creation
    metrics_apply1 = tmp_path / "metrics_apply1.json"
    res = _run_cli([
        "--config", str(config_path),
        "--backend", "sqlite",
        "--dsn", str(db_path),
        "--metrics-out", str(metrics_apply1),
        "--log-level", "INFO",
    ])
    assert res.returncode == 0, f"Apply #1 failed:\nSTDOUT:\n{res.stdout}\nSTDERR:\n{res.stderr}"
    assert metrics_apply1.exists(), "Apply #1 metrics file was not created"

    # Validate DB schema after apply
    tables, indexes = _sqlite_objects(db_path)
    assert "task" in tables, "Entity table 'task' was not created"
    assert "task_dependencies" in tables, "Relationship table 'task_dependencies' was not created"
    assert "idx_task_name" in indexes, "Index 'idx_task_name' was not created"

    # Validate metrics reflect applied changes
    m1 = _read_metrics(metrics_apply1)
    assert m1.get("backend") == "sqlite"
    assert m1.get("dry_run") is False
    c1 = m1.get("counts", {})
    assert c1["entities"]["created"] >= 1
    assert c1["relationships"]["created"] >= 1
    assert c1["indexes"]["created"] >= 1

    # 3) Apply again: must be idempotent (no new creations)
    metrics_apply2 = tmp_path / "metrics_apply2.json"
    res = _run_cli([
        "--config", str(config_path),
        "--backend", "sqlite",
        "--dsn", str(db_path),
        "--metrics-out", str(metrics_apply2),
        "--log-level", "INFO",
    ])
    assert res.returncode == 0, f"Apply #2 (idempotency) failed:\nSTDOUT:\n{res.stdout}\nSTDERR:\n{res.stderr}"
    assert metrics_apply2.exists(), "Apply #2 metrics file was not created"

    # Schema should remain unchanged
    tables2, indexes2 = _sqlite_objects(db_path)
    assert tables2 == tables, "Tables changed on idempotent re-run"
    assert indexes2 == indexes, "Indexes changed on idempotent re-run"

    # Metrics should report no creations, only skipped
    m2 = _read_metrics(metrics_apply2)
    assert m2.get("dry_run") is False
    c2 = m2.get("counts", {})
    assert c2["entities"]["created"] == 0
    assert c2["relationships"]["created"] == 0
    assert c2["indexes"]["created"] == 0
    # Expect skipped to be at least the number of structures previously created
    assert c2["entities"]["skipped"] >= 1
    assert c2["relationships"]["skipped"] >= 1
    assert c2["indexes"]["skipped"] >= 1
