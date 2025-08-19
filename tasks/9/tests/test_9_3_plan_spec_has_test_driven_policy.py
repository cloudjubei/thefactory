import os
import sys

def run():
    path = os.path.join("docs", "PLAN_SPECIFICATION.md")
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    required_phrase = "A feature is not considered complete until a corresponding test is written and passes."
    if "Test-Driven Acceptance" not in content or required_phrase not in content:
        print("FAIL: PLAN_SPECIFICATION.md missing Test-Driven Acceptance section or required phrase.")
        sys.exit(1)

    print("PASS: PLAN_SPECIFICATION.md encodes the test-driven policy.")
    sys.exit(0)

if __name__ == "__main__":
    run()
