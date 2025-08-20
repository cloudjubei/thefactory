import os
import sys

def run():
    print("Running test for Feature 13.11: Remove Migration Guide")
    errors = []

    migration_guide_path = 'docs/tasks/TASKS_MIGRATION_GUIDE.md'
    if os.path.exists(migration_guide_path):
        errors.append(f"FAIL: {migration_guide_path} still exists.")

    if errors:
        for error in errors:
            print(error)
        sys.exit(1)

    print("PASS: Feature 13.11 test checks passed.")
    sys.exit(0)

if __name__ == "__main__":
    run()
