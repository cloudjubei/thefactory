import os, sys

def run():
    print("Running test for Feature 13.10: Remove TASKS.md")
    tasks_md_path = 'tasks/TASKS.md'
    if os.path.exists(tasks_md_path):
        print(f"FAIL: {tasks_md_path} still exists.")
        sys.exit(1)
    
    print("PASS: tasks/TASKS.md has been successfully removed.")
    sys.exit(0)

if __name__ == "__main__":
    run()
