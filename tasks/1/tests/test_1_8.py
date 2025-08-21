import os
import sys
import re


def fail(msg: str):
    print(f"FAIL: {msg}")
    sys.exit(1)


def ok(msg: str):
    print(f"PASS: {msg}")


def main():
    path = os.path.join("docs", "AGENT_DEVELOPER.md")
    if not os.path.isfile(path):
        fail("docs/AGENT_DEVELOPER.md does not exist")
    ok("AGENT_DEVELOPER.md exists")

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Required references
    required_refs = [
        "docs/AGENT_PERSONAS_DEVELOPER.md",
        "docs/FILE_ORGANISATION.md",
        "docs/AGENT_COMMUNICATION_PROTOCOL.md",
        "docs/agent_protocol_example.json",
    ]
    for ref in required_refs:
        if ref not in content:
            fail(f"Reference missing: {ref}")
    ok("All required references present")

    # Tools section and required tool names
    if "Tools" not in content:
        fail("Tools section missing")

    tool_markers = [
        "get_context(",
        "write_file(",
        "run_test(",
        "update_task_status(",
        "update_feature_status(",
        "finish_feature(",
        "finish(",
        "update_agent_question(",
    ]
    for marker in tool_markers:
        if marker not in content:
            fail(f"Tool not documented: {marker}")
    ok("All required tools documented")

    print("ALL CHECKS PASSED for feature 1.8")
    sys.exit(0)


if __name__ == "__main__":
    main()
