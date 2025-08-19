import os
import sys

def run():
    file_path = "scripts/migrate_tasks.py"
    print(f"--- Running Test for Feature 13.7: Check migration script existence ---")

    if not os.path.exists(file_path):
        print(f"FAIL: The migration script {file_path} does not exist.")
        sys.exit(1)
    
    print(f"PASS: Migration script '{file_path}' exists.")
    sys.exit(0)

if __name__ == "__main__":
    run()
