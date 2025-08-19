import os, sys

def run():
    path = "docs/PLAN_SPECIFICATION.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    section_ok = ("Test-Driven Acceptance" in content) or ("## 6. Testing" in content)
    phrase = "A feature is not considered complete until a corresponding test is written and passes."
    if not section_ok:
        print("FAIL: PLAN_SPECIFICATION.md missing the Test-Driven Acceptance section header.")
        sys.exit(1)
    if phrase not in content:
        print("FAIL: PLAN_SPECIFICATION.md missing required policy phrase about test-driven acceptance.")
        sys.exit(1)
    print("PASS: Task 9.4 acceptance verified: Test-Driven Acceptance section and phrase are present.")
    sys.exit(0)

if __name__ == "__main__":
    run()
