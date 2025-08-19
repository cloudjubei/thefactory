import os
import sys
import subprocess


def run():
    # 1) Check docs/AGENT_PERSONAS.md exists
    personas_doc = os.path.join("docs", "AGENT_PERSONAS.md")
    if not os.path.exists(personas_doc):
        print(f"FAIL: {personas_doc} does not exist.")
        sys.exit(1)

    # 2) Check scripts/run_persona.py exists
    runner = os.path.join("scripts", "run_persona.py")
    if not os.path.exists(runner):
        print(f"FAIL: {runner} does not exist.")
        sys.exit(1)

    # 3) Ensure the script provides help and mentions persona names
    try:
        proc = subprocess.run([sys.executable, runner, "--help"], capture_output=True, text=True)
    except Exception as e:
        print(f"FAIL: Could not execute {runner}: {e}")
        sys.exit(1)

    if proc.returncode != 0:
        print(f"FAIL: help command exited with {proc.returncode}. stderr: {proc.stderr}")
        sys.exit(1)

    out = (proc.stdout or "") + (proc.stderr or "")
    expected = ["manager", "planner", "tester", "developer"]
    missing = [w for w in expected if w not in out]
    if missing:
        print(f"FAIL: --help output missing: {', '.join(missing)}")
        sys.exit(1)

    print("PASS: Agent personas doc and runner script exist and are discoverable via --help.")
    sys.exit(0)


if __name__ == "__main__":
    run()
