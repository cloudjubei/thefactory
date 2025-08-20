import os
import sys

def run():
    file_path = 'docs/tasks/task_format.py'
    if not os.path.exists(file_path):
        print(f"FAIL: File '{file_path}' does not exist.")
        sys.exit(1)

    with open(file_path, 'r') as f:
        content = f.read()

    required_defs = [
        "class Feature(TypedDict):",
        "class Task(TypedDict):",
        "id: int",
        "features: List[Feature]"
    ]
    missing_defs = [d for d in required_defs if d not in content]

    if missing_defs:
        print(f"FAIL: File '{file_path}' is missing the following definitions: {', '.join(missing_defs)}")
        sys.exit(1)
        
    print(f"PASS: File '{file_path}' contains the required type definitions.")
    sys.exit(0)

if __name__ == "__main__":
    run()
