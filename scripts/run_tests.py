import sys
import os
import glob
import subprocess


def find_tests():
    return sorted(glob.glob(os.path.join("tasks", "*", "tests", "*.py")))


def run_test(path: str):
    proc = subprocess.run([sys.executable, path], capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr


def main():
    tests = find_tests()
    if not tests:
        print("No tests found under tasks/*/tests/*.py")
        sys.exit(1)

    total = len(tests)
    failed = 0

    for t in tests:
        print(f"Running {t} ...")
        code, out, err = run_test(t)
        if out:
            print(out.strip())
        if err:
            print(err.strip())
        if code != 0:
            print(f"FAIL: {t} exited with code {code}")
            failed += 1
        else:
            print(f"PASS: {t}")

    print(f"\nSummary: {total - failed}/{total} tests passed.")
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
