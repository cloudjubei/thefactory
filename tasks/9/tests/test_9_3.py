import os, sys

def run():
    path = "scripts/run_tests.py"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if "def main()" not in content:
        print("FAIL: scripts/run_tests.py does not define main().")
        sys.exit(1)
    print("PASS: scripts/run_tests.py exists and defines main().")
    sys.exit(0)

if __name__ == "__main__":
    run()
