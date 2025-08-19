import os, sys

def run():
    path = "scripts/run_tests.py"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    required = ["if __name__ == \"__main__\":", "glob.glob", "subprocess.run"]
    missing = [s for s in required if s not in content]
    if missing:
        print("FAIL: run_tests.py missing: " + ", ".join(missing))
        sys.exit(1)
    print("PASS: Task 9.3 acceptance (presence and basic structure) verified.")
    sys.exit(0)

if __name__ == "__main__":
    run()
