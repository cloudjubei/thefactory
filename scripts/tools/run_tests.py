import subprocess
import sys
import json
import re


def run_tests_tool(repo_path: str) -> str:
    """
    Run the project's test suite via scripts/run_tests.py and return results.

    Args:
        repo_path: Absolute path to the cloned repository root.

    Returns:
        JSON string with keys: ok (bool), exit_code (int), stdout (str), stderr (str), passed (int|None), total (int|None)
    """
    try:
        proc = subprocess.run([sys.executable, "scripts/run_tests.py"], cwd=repo_path, capture_output=True, text=True)
        out = proc.stdout or ""
        err = proc.stderr or ""
        code = proc.returncode
        passed = None
        total = None
        m = re.search(r"Summary:\s+(\d+)/(\d+)\s+tests passed\.\s*", out)
        if m:
            passed = int(m.group(1))
            total = int(m.group(2))
        result = {
            "ok": code == 0,
            "exit_code": code,
            "stdout": out,
            "stderr": err,
            "passed": passed,
            "total": total,
        }
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"ok": False, "error": f"Failed to run tests: {e}"})