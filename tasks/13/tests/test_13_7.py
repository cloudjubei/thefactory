import os
import sys

def run():
    file_path = "scripts/migrate_tasks.py"
    print(f"--- Running Test for Feature 13.7: Check migration script existence ---")

    if not os.path.exists(file_path):
        print(f"FAIL: The migration script {file_path} does not exist.")
        sys.exit(1)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'if __name__ == "__main__":' not in content:
            print(f"WARNING: {file_path} may not be a runnable script (missing `if __name__ == '__main__':`).")
    except Exception as e:
        print(f"FAIL: An error occurred while reading {file_path}: {e}")
        sys.exit(1)

    print(f"PASS: The migration script {file_path} exists.")
    sys.exit(0)

if __name__ == "__main__":
    run()
