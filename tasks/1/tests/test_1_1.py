import os
import sys
import ast

def run():
    path = "docs/tasks/task_format.py"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        print(f"FAIL: Could not parse {path}: {e}")
        sys.exit(1)

    class_defs = {node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)}
    
    required_classes = {"Task", "Feature"}
    if not required_classes.issubset(class_defs):
        print(f"FAIL: Missing TypedDicts. Found: {class_defs}, Required: {required_classes}")
        sys.exit(1)

    # Basic check for key fields
    if 'class Task(TypedDict):' not in content.replace(" ", ""):
         print(f"FAIL: 'Task' does not appear to be a TypedDict.")
         sys.exit(1)

    if 'class Feature(TypedDict):' not in content.replace(" ", ""):
         print(f"FAIL: 'Feature' does not appear to be a TypedDict.")
         sys.exit(1)

    print("PASS: docs/tasks/task_format.py exists and defines Task and Feature TypedDicts.")
    sys.exit(0)

if __name__ == "__main__":
    run()
