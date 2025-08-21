import os, sys, json

def fail(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)

def pass_msg(msg):
    print(f"PASS: {msg}")
    sys.exit(0)

def run():
    md_path = "docs/AGENT_COMMUNICATION_PROTOCOL.md"
    json_path = "docs/AGENT_COMMUNICATION_PROTOCOL.json"

    # Check MD file exists and contains key phrases
    if not os.path.exists(md_path):
        fail(f"{md_path} does not exist")
    with open(md_path, "r", encoding="utf-8") as f:
        md = f.read()
    required_phrases = [
        "JSON Response Schema",
        "tool_calls",
        "arguments",
        "plan"
    ]
    missing = [p for p in required_phrases if p not in md]
    if missing:
        fail("MD missing required phrases: " + ", ".join(missing))

    # Check JSON file exists and is a valid JSON object defining the format
    if not os.path.exists(json_path):
        fail(f"{json_path} does not exist")
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            schema = json.load(f)
    except Exception as e:
        fail(f"Invalid JSON in {json_path}: {e}")

    if not isinstance(schema, dict):
        fail("Protocol JSON is not an object")

    # Minimal structural checks
    props = schema.get("properties", {})
    if not isinstance(props, dict):
        fail("Schema 'properties' must be an object")
    if "plan" not in props or "tool_calls" not in props:
        fail("Schema must define 'plan' and 'tool_calls' properties")

    tool_calls = props.get("tool_calls", {})
    items = tool_calls.get("items", {}) if isinstance(tool_calls, dict) else {}
    item_props = items.get("properties", {}) if isinstance(items, dict) else {}
    if "tool_name" not in item_props or "arguments" not in item_props:
        fail("Schema must define 'tool_name' and 'arguments' for each tool call item")

    # If we reached here, all checks passed
    pass_msg("Agent Communication Protocol docs and JSON schema are present and well-formed.")

if __name__ == "__main__":
    run()
