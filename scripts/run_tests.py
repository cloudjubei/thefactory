#!/usr/bin/env python3
import os
import sys
import glob
import subprocess

def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    pattern = os.path.join(repo_root, "tasks", "*", "tests", "*.py")
    test_files = sorted(glob.glob(pattern))

    if not test_files:
        print("No tests found.")
        sys.exit(0)

    total = len(test_files)
    failures = 0
    print(f"Discovered {total} test(s). Running...\n")

    for idx, test in enumerate(test_files, 1):
        rel = os.path.relpath(test, repo_root)
        print(f"[{idx}/{total}] Running {rel} ...")
        result = subprocess.run([sys.executable, rel], cwd=repo_root, capture_output=True, text=True)
        # Forward test output
        if result.stdout:
            print(result.stdout, end="")
        if result.returncode != 0:
            if result.stderr:
                print(result.stderr, end="")
            print(f"FAIL: {rel} exited with code {result.returncode}")
            failures += 1
        else:
            print(f"PASS: {rel}")
        print("-" * 60)

    if failures:
        print(f"Test run completed: {total - failures}/{total} passed, {failures} failed.")
        sys.exit(1)

    print(f"All {total} tests passed.")
    sys.exit(0)

if __name__ == "__main__":
    main()
