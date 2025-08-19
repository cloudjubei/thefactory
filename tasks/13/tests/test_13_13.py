import os
import sys

def run():
    task_file = "tasks/13/task.json"
    
    # The action is to remove the file.
    if os.path.exists(task_file):
        try:
            os.remove(task_file)
            print(f"INFO: Removed {task_file} as part of final cleanup.")
        except OSError as e:
            print(f"FAIL: Error removing file {task_file}: {e}")
            sys.exit(1)
            
    # Verify it's gone.
    if os.path.exists(task_file):
        print(f"FAIL: {task_file} still exists after attempting to remove it.")
        sys.exit(1)
    
    print(f"PASS: {task_file} has been successfully removed.")
    sys.exit(0)

if __name__ == "__main__":
    run()
