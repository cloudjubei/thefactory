import os
import sys
import ast

def run():
    path = "scripts/tools/task_utils.py"
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

    func_defs = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}

    required_funcs = {"get_task", "update_task", "create_task"}
    
    status_update_present = any("status" in func for func in func_defs)
    
    missing_core = required_funcs - func_defs
    if missing_core:
        print(f"FAIL: Missing core functions in {path}: {', '.join(missing_core)}")
        sys.exit(1)
        
    if not status_update_present:
        print(f"FAIL: No status update functions found in {path}.")
        sys.exit(1)

    print(f"PASS: {path} exists and defines the required utility functions.")
    sys.exit(0)

if __name__ == "__main__":
    run()
