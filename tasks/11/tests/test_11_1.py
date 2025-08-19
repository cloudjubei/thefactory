import os, sys, re


def fail(msg: str):
    print(f"FAIL: {msg}")
    sys.exit(1)


def run():
    path = "docs/TASKS_JSON_FORMAT.md"
    if not os.path.exists(path):
        fail(f"{path} does not exist.")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Folder structure elements
    for needle in ["tasks/{id}/", "task.json", "plan_{id}.md", "tests/"]:
        if needle not in content:
            fail(f"Missing folder structure element: '{needle}'")
    if "artifacts" not in content:
        fail("Missing mention of optional 'artifacts' folder")

    # Core fields
    fields = [
        "id", "status", "title", "action", "acceptance", "notes", "dependencies",
        "features", "metadata", "created", "updated", "version"
    ]
    missing = [f for f in fields if re.search(rf"\\b{re.escape(f)}\\b", content) is None]
    if missing:
        fail("Missing schema field mentions: " + ", ".join(missing))

    # Reference to status definitions
    if "docs/TASK_FORMAT.md" not in content:
        fail("Must reference docs/TASK_FORMAT.md for status codes")

    # Example presence
    if not re.search(r"example", content, re.IGNORECASE):
        fail("No example section found (expected an end-to-end example)")

    print("PASS: TASKS_JSON_FORMAT.md meets required structure and references.")
    sys.exit(0)


if __name__ == "__main__":
    run()
