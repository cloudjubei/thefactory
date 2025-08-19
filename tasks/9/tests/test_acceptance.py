import os, sys, glob

def run_test():
    # Verify Plan Specification mandates test-driven acceptance
    plan_path = "docs/PLAN_SPECIFICATION.md"
    if not os.path.exists(plan_path):
        print(f"FAIL: {plan_path} does not exist.")
        sys.exit(1)
    content = open(plan_path, "r", encoding="utf-8").read()
    if "Test-Driven Acceptance" not in content:
        print("FAIL: PLAN_SPECIFICATION.md missing 'Test-Driven Acceptance' section.")
        sys.exit(1)
    phrases = [
        "not considered complete until a corresponding test is written and passes",
        "A feature is not considered complete until a corresponding test is written and passes"
    ]
    if not any(p in content for p in phrases):
        print("FAIL: PLAN_SPECIFICATION.md missing wording that a feature requires a test that passes.")
        sys.exit(1)

    # Verify that per-task tests exist for Tasks 1–8
    missing_dirs = []
    missing_files = []
    for task_id in range(1, 9):
        tdir = f"tasks/{task_id}/tests"
        if not os.path.isdir(tdir):
            missing_dirs.append(tdir)
            continue
        py_tests = glob.glob(os.path.join(tdir, "*.py"))
        if not py_tests:
            missing_files.append(tdir)
    if missing_dirs or missing_files:
        if missing_dirs:
            print("FAIL: Missing test directories: " + ", ".join(missing_dirs))
        if missing_files:
            print("FAIL: Missing test files in: " + ", ".join(missing_files))
        sys.exit(1)

    print("PASS: Task 9 meta-acceptance verified: policy present and tests exist for Tasks 1–8.")
    sys.exit(0)

if __name__ == "__main__":
    run_test()
