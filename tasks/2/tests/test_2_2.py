import os
import sys

def run():
    print("Running test for feature 2.2: Dependency specification")
    file_path = "requirements.txt"
    if not os.path.exists(file_path):
        print(f"FAIL: {file_path} does not exist.")
        sys.exit(1)
    
    print(f"PASS: {file_path} exists.")
    sys.exit(0)

if __name__ == "__main__":
    run()
