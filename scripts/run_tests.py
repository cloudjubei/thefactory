import os
import sys
import subprocess
import glob


def discover_tests():
    pattern = os.path.join("tasks", "*", "tests", "*.py")
    files = sorted(glob.glob(pattern))
    return files


def run_test(test_path: str) -> tuple[bool, str]:
    try:
        proc = subprocess.run([sys.executable, test_path], capture_output=True, text=True)
        ok = proc.returncode == 0
        output = (proc.stdout or "") + (proc.stderr or "")
        return ok, output
    except Exception as e:
        return False, f"Exception while running {test_path}: {e}"


def main():
    tests = discover_tests()
    if not tests:
        print("No tests found under tasks/*/tests/*.py")
        sys.exit(1)

    total = len(tests)
    passed = 0
    failed = 0

    print(f"Discovered {total} tests. Running...\n")

    for t in tests:
        ok, output = run_test(t)
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {t}")
        if output.strip():
            print(output.strip())
        print("-")
        if ok:
            passed += 1
        else:
            failed += 1

    print(f"\nSummary: {passed} passed, {failed} failed, {total} total")
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
