import os
import sys

def run():
    print("Checking test for feature 3.2: projects directory and .gitignore")

    # Check for projects directory
    projects_dir = "projects"
    if not os.path.isdir(projects_dir):
        print(f"FAIL: Directory '{projects_dir}' does not exist.")
        sys.exit(1)
    
    # Check .gitignore content
    gitignore_path = ".gitignore"
    if not os.path.exists(gitignore_path):
        print(f"FAIL: {gitignore_path} does not exist.")
        sys.exit(1)

    with open(gitignore_path, "r", encoding="utf-8") as f:
        content = f.read()

    if "/projects/" not in content.splitlines():
        print(f"FAIL: '/projects/' not found in {gitignore_path}.")
        sys.exit(1)
    
    print("PASS: 'projects/' directory exists and is listed in .gitignore.")
    sys.exit(0)

if __name__ == "__main__":
    run()
