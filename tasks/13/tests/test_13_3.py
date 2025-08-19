import os
import sys

def run():
    file_path = "docs/tasks/TASKS_MIGRATION_GUIDE.md"
    print(f"--- Running Test for Feature 13.3: Check {file_path} ---")

    # 1. Check if file exists
    if not os.path.exists(file_path):
        print(f"FAIL: {file_path} does not exist.")
        sys.exit(1)
    
    print(f"PASS: File '{file_path}' exists.")

    # 2. Check for required sections
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    required_headings = [
        "# TASKS.md to JSON Migration Guide",
        "## 1. Migration Plan",
        "## 2. Backward Compatibility Strategy",
        "## 3. Tooling Requirements",
        "## 4. Rollback Plan"
    ]
    
    missing_headings = [h for h in required_headings if h not in content]

    if missing_headings:
        print(f"FAIL: Missing required headings in {file_path}: {', '.join(missing_headings)}")
        sys.exit(1)

    print(f"PASS: All required headings are present in the migration guide.")
    
    print(f"--- Test for Feature 13.3 PASSED ---")
    sys.exit(0)

if __name__ == "__main__":
    run()
