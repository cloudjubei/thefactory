import os, sys

def run():
    path = "docs/AGENT_PRINCIPLES.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Validate key expectations per acceptance
    checks = [
        ("mentions Agent", "Agent" in content),
        ("mentions Orchestrator", "Orchestrator" in content),
        ("references tools guide", "TOOL_ARCHITECTURE.md" in content or "docs/TOOL_ARCHITECTURE.md" in content),
    ]

    failures = [name for name, ok in checks if not ok]
    if failures:
        print("FAIL: AGENT_PRINCIPLES.md missing: " + ", ".join(failures))
        sys.exit(1)

    print("PASS: AGENT_PRINCIPLES.md defines Agent vs Orchestrator and references the tools guide.")
    sys.exit(0)

if __name__ == "__main__":
    run()
