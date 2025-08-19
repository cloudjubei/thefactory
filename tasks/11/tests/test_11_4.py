import os, sys


def fail(msg: str):
    print(f"FAIL: {msg}")
    sys.exit(1)


def expect_line(content: str, needle: str):
    if needle not in content:
        fail(f"Missing task line: {needle}")


def run():
    path = "tasks/TASKS.md"
    if not os.path.exists(path):
        fail(f"{path} does not exist.")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    expect_line(content, "25) - Implement JSON schemas and validation tooling")
    expect_line(content, "26) - Update orchestrator for task.json and persona-scoped context")
    expect_line(content, "27) - Migrate existing tasks to per-folder JSON files")
    expect_line(content, "28) - Remove legacy TASKS.md and finalize documentation")

    print("PASS: Tasks 25–28 exist and are pending with correct titles.")
    sys.exit(0)


if __name__ == "__main__":
    run()
