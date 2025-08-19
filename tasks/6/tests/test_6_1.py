import os, sys

def run():
    path = "docs/TOOL_ARCHITECTURE.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    required_headings = [
        "# Tool-Using Agent Architecture",
        "## 1. Core Principle",
        "## 2. Agent-Orchestrator Contract",
        "## 3. JSON Response Schema",
        "## 4. Available Tools",
        "## 5. Execution Modes",
        "## 6. Mandatory Task Completion Workflow",
    ]
    missing_heads = [h for h in required_headings if h not in content]

    required_tools = [
        "### `write_file`",
        "### `retrieve_context_files`",
        "### `rename_files`",
        "### `run_tests`",
        "### `finish_feature`",
        "### `submit_for_review`",
        "### `ask_question`",
        "### `finish`",
        "### `read_plan_feature`",
        "### `update_feature_status`",
    ]
    missing_tools = [t for t in required_tools if t not in content]

    # Schema keys presence
    schema_keys_ok = ('"plan"' in content or "\"plan\"" in content) and ('"tool_calls"' in content or "\"tool_calls\"" in content)

    problems = []
    if missing_heads:
        problems.append("Missing headings: " + ", ".join(missing_heads))
    if missing_tools:
        problems.append("Missing tool definitions: " + ", ".join(missing_tools))
    if not schema_keys_ok:
        problems.append("JSON schema keys 'plan' and/or 'tool_calls' not found")

    if problems:
        print("FAIL: TOOL_ARCHITECTURE.md issues: " + " | ".join(problems))
        sys.exit(1)

    print("PASS: TOOL_ARCHITECTURE.md exists with required sections and tool definitions.")
    sys.exit(0)

if __name__ == "__main__":
    run()
