import os, sys

def run():
    path = "docs/TASKS_JSON_FORMAT.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    required_strings = [
        "tasks/{id}/", "task.json", "plan_{id}.md", "tests/", "artifacts",
        "id (int)", "status (one of + ~ - ? / =)", "title (string)", "action (string)",
        "acceptance (array[string] or structured list)", "notes (string, optional)",
        "dependencies (array[int], optional)", "features (array[Feature])",
        "metadata (object: created, updated, version)",
        "number", "context", "output", "notes",
        "docs/TASK_FORMAT.md", "Example: task.json"
    ]

    missing = [s for s in required_strings if s not in content]
    if missing:
        print("FAIL: Missing required phrases: " + ", ".join(missing))
        sys.exit(1)

    print("PASS: TASKS_JSON_FORMAT.md defines required structure, fields, references, and examples.")
    sys.exit(0)

if __name__ == "__main__":
    run()
