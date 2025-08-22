import pytest


def make_fixtures():
    # Legacy data: id 1 has no parent; 2 and 3 are children of 1; 4 is child of 2
    # 5 is invalid (self-parent); 6 has missing parent 999
    return [
        {"id": 1, "legacy_parent_id": None},
        {"id": 2, "legacy_parent_id": 1},
        {"id": 3, "legacy_parent_id": 1},
        {"id": 4, "legacy_parent_id": 2},
        {"id": 5, "legacy_parent_id": 5},
        {"id": 6, "legacy_parent_id": 999},
    ]


class FakeFetcher:
    def __init__(self, data):
        self.data = data
        self.calls = []

    def __call__(self, resume_from, batch_size):
        self.calls.append({"resume_from": resume_from, "batch_size": batch_size})
        filtered = [row for row in self.data if resume_from is None or row["id"] > resume_from]
        for i in range(0, len(filtered), batch_size):
            yield filtered[i : i + batch_size]


class FakeWriter:
    def __init__(self, existing_relations=None, existing_projects=None):
        self.created = set()
        self.begin_calls = 0
        self.commit_calls = 0
        self.existing_relations = set(existing_relations or [])
        # If existing_projects is None, assume all projects exist when checked
        self.projects = set(existing_projects) if existing_projects is not None else None

    def exists_project(self, project_id):
        if self.projects is None:
            return True
        return project_id in self.projects

    def relation_exists(self, parent_id, child_id):
        return (
            (parent_id, child_id) in self.created
            or (parent_id, child_id) in self.existing_relations
        )

    def create_relation(self, parent_id, child_id):
        self.created.add((parent_id, child_id))

    # Optional batch hooks
    def begin_batch(self):
        self.begin_calls += 1

    def commit_batch(self):
        self.commit_calls += 1


class FakeAuditor:
    def __init__(self):
        self.logs = []

    def log(self, action, details):
        self.logs.append((action, details))


class FakeLogger:
    def __init__(self):
        self.messages = {"info": [], "error": [], "warning": []}

    def info(self, msg):
        self.messages["info"].append(str(msg))

    def error(self, msg):
        self.messages["error"].append(str(msg))

    def warning(self, msg):
        self.messages["warning"].append(str(msg))


def test_migrate_child_projects_end_to_end():
    # Requires scripts.migrate_child_projects module with migrate entrypoint
    from scripts import migrate_child_projects as mod

    data = make_fixtures()
    fetcher = FakeFetcher(data)
    # All projects exist except the missing parent referenced by id=6
    all_existing_projects = {row["id"] for row in data if row["legacy_parent_id"] != 999}
    writer = FakeWriter(existing_projects=all_existing_projects)
    auditor = FakeAuditor()
    logger = FakeLogger()

    summary = mod.migrate(
        fetcher=fetcher,
        writer=writer,
        auditor=auditor,
        batch_size=2,
        dry_run=False,
        resume_from=None,
        logger=logger,
    )

    # Summary expectations
    assert summary["dry_run"] is False
    # 5 candidates (ids 2,3,4,5,6) with non-null legacy_parent_id
    assert summary["processed"] == 5
    assert summary["created"] == 3
    assert summary["skipped_existing"] == 0
    assert summary["failed"] == 2
    assert summary["checkpoint"] == 6

    # Relations created correctly
    assert writer.created == {(1, 2), (1, 3), (2, 4)}

    # Optional batch hooks should be invoked per batch (3 batches of size 2 => 3 batches overall)
    assert writer.begin_calls == 3
    assert writer.commit_calls == 3

    # Auditing for created relations
    audit_actions = [a for a, _ in auditor.logs]
    assert audit_actions.count("child_project_backfill") == 3
    for action, details in auditor.logs:
        assert action == "child_project_backfill"
        assert details.get("parent_id") in {1, 2}
        assert details.get("child_id") in {2, 3, 4}
        assert details.get("source") == "legacy"

    # Data integrity equation holds
    assert summary["processed"] == summary["created"] + summary["skipped_existing"] + summary["failed"]

    # Logging occurred
    assert any("batch" in msg.lower() for msg in logger.messages["info"]) or len(logger.messages["info"]) > 0
    assert len(logger.messages["error"]) >= 1  # invalid records should log errors


def test_migrate_is_idempotent_and_supports_dry_run_and_resume():
    from scripts import migrate_child_projects as mod

    data = make_fixtures()

    # First run creates baseline relations
    fetcher1 = FakeFetcher(data)
    writer1 = FakeWriter(existing_projects={1, 2, 3, 4, 5, 6})
    auditor1 = FakeAuditor()
    logger1 = FakeLogger()
    summary1 = mod.migrate(
        fetcher=fetcher1,
        writer=writer1,
        auditor=auditor1,
        batch_size=100,
        dry_run=False,
        resume_from=None,
        logger=logger1,
    )
    assert summary1["created"] == 3

    # Second run is idempotent: no new creations, all relations reported as skipped_existing
    fetcher2 = FakeFetcher(data)
    summary2 = mod.migrate(
        fetcher=fetcher2,
        writer=writer1,
        auditor=auditor1,
        batch_size=100,
        dry_run=False,
        resume_from=None,
        logger=logger1,
    )
    assert summary2["created"] == 0
    assert summary2["skipped_existing"] == 3

    # Dry-run mode: should not call create_relation
    fetcher3 = FakeFetcher(data)
    writer_dry = FakeWriter(existing_projects={1, 2, 3, 4, 5, 6})
    dry_summary = mod.migrate(
        fetcher=fetcher3,
        writer=writer_dry,
        auditor=auditor1,
        batch_size=100,
        dry_run=True,
        resume_from=None,
        logger=logger1,
    )
    assert dry_summary["dry_run"] is True
    assert dry_summary["created"] == 0
    assert writer_dry.created == set()

    # Resume support: only process records with id > resume_from
    fetcher4 = FakeFetcher(data)
    writer_resume = FakeWriter(existing_projects={1, 2, 3, 4, 5, 6})
    resume_summary = mod.migrate(
        fetcher=fetcher4,
        writer=writer_resume,
        auditor=auditor1,
        batch_size=2,
        dry_run=False,
        resume_from=3,
        logger=logger1,
    )
    # For ids > 3 => rows 4,5,6: creates (2,4), fails 2; processed 3
    assert resume_summary["processed"] == 3
    assert resume_summary["created"] == 1
    assert resume_summary["failed"] == 2
    assert (2, 4) in writer_resume.created

    # Fetcher should have been called with resume_from=3
    assert fetcher4.calls and fetcher4.calls[0]["resume_from"] == 3


def test_self_parent_and_missing_parent_are_rejected():
    from scripts import migrate_child_projects as mod

    data = [
        {"id": 10, "legacy_parent_id": 10},  # self-parent
        {"id": 11, "legacy_parent_id": 9999},  # missing parent
    ]
    fetcher = FakeFetcher(data)
    writer = FakeWriter(existing_projects={11})  # only child exists
    auditor = FakeAuditor()
    logger = FakeLogger()

    summary = mod.migrate(
        fetcher=fetcher,
        writer=writer,
        auditor=auditor,
        batch_size=1,
        dry_run=False,
        resume_from=None,
        logger=logger,
    )

    assert summary["created"] == 0
    assert summary["failed"] == 2
    assert writer.created == set()
    assert len(logger.messages["error"]) >= 2
