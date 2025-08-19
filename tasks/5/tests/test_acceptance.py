import os, sys

def run_test():
    path = "docs/PLAN_SPECIFICATION.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    content = open(path, "r", encoding="utf-8").read()
    required_any = [
        "Test-Driven Acceptance",
    ]
    # also confirm general presence
    required = [
        "# Plan Specification",
        "Purpose",
        "Core Principles",
        "Location and Structure",
        "Template",
        "Example"
    ]
    missing = [s for s in required if s not in content]
    if missing:
        print(f"FAIL: {path} missing: {', '.join(missing)}")
        sys.exit(1)
    if not any(s in content for s in required_any):
        print(f"FAIL: {path} missing test-driven policy reference.")
        sys.exit(1)
    print("PASS: Task 5 acceptance verified.")
    sys.exit(0)

if __name__ == "__main__":
    run_test()
