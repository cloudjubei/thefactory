import os
import sys

def run():
    guide_path = "docs/tasks/TASKS_MIGRATION_GUIDE.md"
    if not os.path.exists(guide_path):
        print("PASS: TASKS_MIGRATION_GUIDE.md has been correctly removed.")
        sys.exit(0)
    else:
        print(f"FAIL: TASKS_MIGRATION_GUIDE.md still exists.")
        sys.exit(1)

if __name__ == "__main__":
    run()
