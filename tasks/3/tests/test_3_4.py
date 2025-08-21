import os
import sys
import shutil
import importlib.util
import subprocess

def cleanup(test_project_path, gitmodules_path, original_gitmodules_content):
    print("Cleaning up test artifacts...")
    if os.path.exists(test_project_path):
        shutil.rmtree(test_project_path)
    
    if original_gitmodules_content is not None:
        with open(gitmodules_path, "w") as f:
            f.write(original_gitmodules_content)
    elif os.path.exists(gitmodules_path):
        try:
            subprocess.run(
                ['git', 'ls-files', '--error-unmatch', gitmodules_path],
                check=True, capture_output=True, text=True
            )
        except subprocess.CalledProcessError:
            os.remove(gitmodules_path)
    print("Cleanup finished.")

def run():
    print("Checking test for feature 3.4: Child project initialization script")
    
    script_path = "scripts/project_manager.py"
    test_project_name = "_test_child_project_12345"
    test_project_path = os.path.join("projects", test_project_name)
    gitmodules_path = ".gitmodules"
    original_gitmodules_content = None

    if os.path.exists(gitmodules_path):
        with open(gitmodules_path, 'r') as f:
            original_gitmodules_content = f.read()

    if os.path.exists(test_project_path):
        shutil.rmtree(test_project_path)
    
    if not os.path.exists(script_path):
        print(f"FAIL: Script file '{script_path}' does not exist.")
        sys.exit(1)

    if not os.path.exists('templates/child_project'):
        print("FAIL: Prerequisite from feature 3.3 (templates/child_project) not met. Cannot test feature 3.4.")
        sys.exit(1)

    try:
        spec = importlib.util.spec_from_file_location("project_manager", script_path)
        project_manager = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(project_manager)
        create_child_project_func = getattr(project_manager, 'create_child_project')
    except Exception as e:
        print(f"FAIL: Could not import or inspect {script_path}. Error: {e}")
        sys.exit(1)

    try:
        print(f"Attempting to create child project '{test_project_name}'...")
        create_child_project_func(test_project_name)

        if not os.path.isdir(test_project_path):
            print(f"FAIL: Project directory '{test_project_path}' was not created.")
            cleanup(test_project_path, gitmodules_path, original_gitmodules_content)
            sys.exit(1)
        
        expected_files = ["README.md", ".gitignore", "spec.md"]
        for f in expected_files:
            if not os.path.exists(os.path.join(test_project_path, f)):
                print(f"FAIL: Expected file '{f}' not found in '{test_project_path}'.")
                cleanup(test_project_path, gitmodules_path, original_gitmodules_content)
                sys.exit(1)

        with open(os.path.join(test_project_path, "README.md"), 'r') as f:
            readme_content = f.read()
        if '{{PROJECT_NAME}}' in readme_content:
            print(f"FAIL: Placeholder '{{{{PROJECT_NAME}}}}' was not replaced in README.md.")
            cleanup(test_project_path, gitmodules_path, original_gitmodules_content)
            sys.exit(1)
        if test_project_name not in readme_content:
            print(f"FAIL: Project name '{test_project_name}' not found in README.md.")
            cleanup(test_project_path, gitmodules_path, original_gitmodules_content)
            sys.exit(1)
            
        if not os.path.isdir(os.path.join(test_project_path, ".git")):
            print(f"FAIL: Git repository was not initialized in '{test_project_path}'.")
            cleanup(test_project_path, gitmodules_path, original_gitmodules_content)
            sys.exit(1)

        if not os.path.exists(gitmodules_path):
            print("FAIL: .gitmodules file was not created in the root directory.")
            cleanup(test_project_path, gitmodules_path, original_gitmodules_content)
            sys.exit(1)

        with open(gitmodules_path, 'r') as f:
            gitmodules_content = f.read()
        
        expected_submodule_entry = f'[submodule "projects/{test_project_name}"]'
        if expected_submodule_entry not in gitmodules_content:
            print(f"FAIL: Submodule entry for '{test_project_name}' not found in .gitmodules.")
            cleanup(test_project_path, gitmodules_path, original_gitmodules_content)
            sys.exit(1)
        
        print("PASS: Child project initialization script works as expected.")
        cleanup(test_project_path, gitmodules_path, original_gitmodules_content)
        sys.exit(0)

    except Exception as e:
        import traceback
        print(f"FAIL: Execution of create_child_project failed with an error: {e}")
        traceback.print_exc()
        cleanup(test_project_path, gitmodules_path, original_gitmodules_content)
        sys.exit(1)

if __name__ == "__main__":
    run()
