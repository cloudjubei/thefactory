import os, sys, re


def fail(msg: str):
    print(f"FAIL: {msg}")
    sys.exit(1)


def run():
    path = "docs/TASKS_MIGRATION_GUIDE.md"
    if not os.path.exists(path):
        fail(f"{path} does not exist.")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Dual-read compatibility
    if not ("dual-read" in content or re.search(r"dual\\s*read", content, re.IGNORECASE)):
        fail("Missing 'dual-read' compatibility mention")

    # Orchestrator and persona-scoped context
    if "scripts/run_local_agent.py" not in content and "orchestrator" not in content:
        fail("Missing orchestrator reference (scripts/run_local_agent.py or 'orchestrator')")
    if not ("persona-scoped" in content or ("persona" in content and "context" in content)):
        fail("Missing persona-scoped context requirement")

    # Testing/CI references
    if "docs/TESTING.md" not in content:
        fail("Missing reference to docs/TESTING.md for CI/schema validation")

    # Rollback and deprecation
    if not re.search(r"rollback", content, re.IGNORECASE):
        fail("Missing rollback plan mention")
    if not re.search(r"deprecat", content, re.IGNORECASE):
        fail("Missing deprecation strategy mention")

    print("PASS: TASKS_MIGRATION_GUIDE.md covers dual-read, orchestrator context, CI, rollback, and deprecation.")
    sys.exit(0)


if __name__ == "__main__":
    run()
