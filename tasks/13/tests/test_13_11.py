import os, sys

def run():
    print("Running test for Feature 13.11: Remove Migration Guide")
    path = 'docs/tasks/TASKS_MIGRATION_GUIDE.md'
    if os.path.exists(path):
        print(f"FAIL: {path} still exists.")
        sys.exit(1)
    
    print("PASS: docs/tasks/TASKS_MIGRATION_GUIDE.md has been successfully removed.")
    sys.exit(0)

if __name__ == "__main__":
    run()
