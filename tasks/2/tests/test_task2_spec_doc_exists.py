import os
import sys

def run():
    spec_path = os.path.join("docs", "SPEC.md")
    if not os.path.exists(spec_path):
        print(f"FAIL: {spec_path} does not exist.")
        sys.exit(1)

    with open(spec_path, "r", encoding="utf-8") as f:
        content = f.read()

    if "SPECIFICATION_GUIDE.md" not in content:
        print("FAIL: docs/SPEC.md does not reference SPECIFICATION_GUIDE.md.")
        sys.exit(1)

    print("PASS: SPEC.md exists and references SPECIFICATION_GUIDE.md.")
    sys.exit(0)

if __name__ == "__main__":
    run()
