import os
import sys

def run():
    file_path = "tasks/TASKS.md"
    print(f"--- Running Test for Feature 13.10: Check removal of {file_path} ---")

    if os.path.exists(file_path):
        print(f"FAIL: The old tasks file {file_path} still exists.")
        sys.exit(1)

    print(f"PASS: {file_path} has been successfully removed.")
    sys.exit(0)

if __name__ == "__main__":
    run()
