import os
import sys

def run():
    print("Checking test for feature 3.3: Child project boilerplate")
    
    base_dir = "templates/child_project"
    
    if not os.path.isdir(base_dir):
        print(f"FAIL: Directory '{base_dir}' does not exist.")
        sys.exit(1)

    required_files = ["README.md", ".gitignore", "spec.md"]
    for filename in required_files:
        path = os.path.join(base_dir, filename)
        if not os.path.exists(path):
            print(f"FAIL: Boilerplate file '{path}' does not exist.")
            sys.exit(1)

    # Check for placeholder in README.md
    readme_path = os.path.join(base_dir, "README.md")
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    if "{{PROJECT_NAME}}" not in content:
        print(f"FAIL: Placeholder '{{{{PROJECT_NAME}}}}' not found in {readme_path}.")
        sys.exit(1)

    print("PASS: Boilerplate directory and files exist with correct content.")
    sys.exit(0)

if __name__ == "__main__":
    run()
