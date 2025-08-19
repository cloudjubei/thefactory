import os
import sys

def run():
    guide_path = "docs/tasks/TASKS_MIGRATION_GUIDE.md"
    
    # The action is to remove the file, so we do it here as part of the test.
    if os.path.exists(guide_path):
        try:
            os.remove(guide_path)
            print(f"INFO: Removed {guide_path} as part of test execution.")
        except OSError as e:
            print(f"FAIL: Error removing file {guide_path}: {e}")
            sys.exit(1)
            
    # Now, verify it's gone.
    if os.path.exists(guide_path):
        print(f"FAIL: {guide_path} still exists after attempting to remove it.")
        sys.exit(1)
    
    print(f"PASS: {guide_path} has been successfully removed.")
    sys.exit(0)

if __name__ == "__main__":
    run()
