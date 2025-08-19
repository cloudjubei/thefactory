import os, sys

def run():
    path = "docs/PLAN_SPECIFICATION.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    phrase = "A feature is not considered complete until a corresponding test is written and passes."
    if phrase not in content:
        print("FAIL: PLAN_SPECIFICATION.md missing exact test-driven policy phrase.")
        sys.exit(1)
    print("PASS: Task 9.4 acceptance verified.")
    sys.exit(0)

if __name__ == "__main__":
    run()
