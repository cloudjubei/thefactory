import os
import sys

def fail(msg: str):
    print(f"FAIL: {msg}")
    sys.exit(1)

def pass_msg(msg: str):
    print(f"PASS: {msg}")
    sys.exit(0)

def run_test():
    plan_path = "docs/PLAN_SPECIFICATION.md"
    if not os.path.exists(plan_path):
        fail(f"{plan_path} does not exist.")

    with open(plan_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1) Must include the named principle
    if "Test-Driven Acceptance" not in content:
        fail("'Test-Driven Acceptance' principle not found in PLAN_SPECIFICATION.md")

    # 2) Must reference docs/TESTING.md
    if "docs/TESTING.md" not in content:
        fail("Reference to docs/TESTING.md not found in PLAN_SPECIFICATION.md")

    # 3) Template/example must require per-feature tests under tasks/{task_id}/tests/
    #    Check for explicit template language and path reference.
    requires_tests_phrase = "Create the test(s)"
    tests_dir_reference = "tasks/{task_id}/tests/"
    naming_convention_example = "test_{task_id}_{feature_number}.py"

    if requires_tests_phrase not in content:
        fail("Template/example does not clearly require creating tests (missing 'Create the test(s)' phrase)")

    if (tests_dir_reference not in content) and (naming_convention_example not in content):
        fail("Template/example does not reference tasks/{task_id}/tests/ or the test naming convention")

    pass_msg("PLAN_SPECIFICATION.md includes Test-Driven Acceptance, references docs/TESTING.md, and mandates per-feature tests in tasks/{task_id}/tests/.")

if __name__ == "__main__":
    run_test()
