import os
import sys


def run_test():
    path = "scripts/run_local_agent.py"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if "class Agent" not in content:
        print("FAIL: run_local_agent.py does not define Agent class.")
        sys.exit(1)
    print("PASS: run_local_agent.py exists and contains Agent class.")
    sys.exit(0)


if __name__ == "__main__":
    run_test()
