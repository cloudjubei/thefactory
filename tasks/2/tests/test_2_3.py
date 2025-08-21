import os
import sys

def run():
    print("Running test for feature 2.3: Environment variables template")
    file_path = ".env.example"
    if not os.path.exists(file_path):
        print(f"FAIL: {file_path} does not exist.")
        sys.exit(1)

    with open(file_path, 'r') as f:
        content = f.read()
    
    if '=' not in content:
        print(f"FAIL: {file_path} does not appear to contain any variable assignments.")
        sys.exit(1)

    print(f"PASS: {file_path} exists and contains variable assignments.")
    sys.exit(0)

if __name__ == "__main__":
    run()
