import os, sys

def run():
    path = "docs/PLAN_SPECIFICATION.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    required_phrase = "Legacy Tasks and Backfilled Plans"
    if required_phrase not in content:
        print(f"FAIL: PLAN_SPECIFICATION.md missing section: '{required_phrase}'.")
        sys.exit(1)
    print("PASS: PLAN_SPECIFICATION.md includes Legacy/Backfill section.")
    sys.exit(0)

if __name__ == "__main__":
    run()
