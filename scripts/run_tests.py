import os
import sys
import glob
import subprocess


def find_repo_root():
    # Assume this script lives in scripts/; repo root is parent of scripts
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def run_test_file(python_exec, test_path, cwd):
    proc = subprocess.run([python_exec, test_path], cwd=cwd)
    return proc.returncode


def main():
    repo_root = find_repo_root()
    pattern = os.path.join(repo_root, "tasks", "*", "tests", "*.py")
    test_files = sorted(glob.glob(pattern))

    if not test_files:
        print("No tests found.")
        sys.exit(0)

    python_exec = sys.executable or "python3"
    total = len(test_files)
    passed = 0
    failed = 0
    failures = []

    print(f"Discovered {total} test(s). Running...\n")

    for test in test_files:
        rel = os.path.relpath(test, repo_root)
        print(f"=== Running {rel} ===")
        code = run_test_file(python_exec, test, repo_root)
        if code == 0:
            print(f"PASS: {rel}\n")
            passed += 1
        else:
            print(f"FAIL: {rel} (exit code {code})\n")
            failed += 1
            failures.append(rel)

    print("Summary:")
    print(f"  Passed: {passed}")
    print(f"  Failed: {failed}")
    print(f"  Total:  {total}")

    if failures:
        print("\nFailures:")
        for f in failures:
            print(f" - {f}")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
