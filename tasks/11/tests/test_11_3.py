import os, sys, re


def fail(msg: str):
    print(f"FAIL: {msg}")
    sys.exit(1)


def run():
    path = "docs/TASK_FORMAT.md"
    if not os.path.exists(path):
        fail(f"{path} does not exist.")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Canonical reference to JSON format
    if "docs/TASKS_JSON_FORMAT.md" not in content:
        fail("Missing reference to docs/TASKS_JSON_FORMAT.md")
    if not re.search(r"canonical", content, re.IGNORECASE):
        fail("Missing mention that JSON format is canonical")

    # Compatibility section referencing TASKS.md and migration guide
    if not re.search(r"compatib", content, re.IGNORECASE):
        fail("Missing compatibility section/mention")
    if "tasks/TASKS.md" not in content:
        fail("Missing mention of legacy tasks/TASKS.md during migration")
    if "docs/TASKS_MIGRATION_GUIDE.md" not in content:
        fail("Missing link/mention of docs/TASKS_MIGRATION_GUIDE.md")

    print("PASS: TASK_FORMAT.md updated to reference JSON canonical format and compatibility guidance.")
    sys.exit(0)


if __name__ == "__main__":
    run()
