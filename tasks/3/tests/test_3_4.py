import os
import sys
import shutil
from pathlib import Path


def fail(msg: str):
    print(f"FAIL: {msg}")
    sys.exit(1)


def pass_msg(msg: str):
    print(f"PASS: {msg}")
    sys.exit(0)


def run():
    # Import the module
    try:
        import scripts.project_manager as pm
    except Exception as e:
        fail(f"Could not import scripts.project_manager: {e}")

    # Validate function exists
    if not hasattr(pm, "create_child_project") or not callable(pm.create_child_project):
        fail("create_child_project function not found or not callable in scripts/project_manager.py")

    repo_root = Path(pm.__file__).resolve().parent.parent

    # Ensure templates exist (dependency from feature 3.3)
    templates_dir = repo_root / "templates" / "child_project"
    expected_templates = [templates_dir / "README.md", templates_dir / ".gitignore", templates_dir / "spec.md"]
    if not templates_dir.exists():
        fail(f"Templates directory missing: {templates_dir}")
    for t in expected_templates:
        if not t.exists():
            fail(f"Template file missing: {t}")

    # Prepare test project name and ensure clean state
    project_name = "test_child_project_init"
    target_dir = repo_root / "projects" / project_name
    if target_dir.exists():
        shutil.rmtree(target_dir)

    # Monkeypatch subprocess.run to avoid executing git commands and to capture calls
    captured = {"calls": []}

    def fake_run(args, cwd=None, check=False, capture_output=False, text=False):
        captured["calls"].append({"args": list(args), "cwd": str(cwd) if cwd else None})
        class Res:
            returncode = 0
            stdout = ""
            stderr = ""
        return Res()

    original_run = pm.subprocess.run
    pm.subprocess.run = fake_run

    try:
        # Execute the function
        pm.create_child_project(project_name)

        # Validate directory and files created
        if not target_dir.exists():
            fail(f"Child project directory not created: {target_dir}")

        for fname in ["README.md", ".gitignore", "spec.md"]:
            fpath = target_dir / fname
            if not fpath.exists():
                fail(f"Expected file not found in child project: {fpath}")

        # Validate placeholder replacement in README.md and spec.md
        for fname in ["README.md", "spec.md"]:
            fpath = target_dir / fname
            try:
                content = fpath.read_text(encoding="utf-8")
            except Exception as e:
                fail(f"Failed reading {fpath}: {e}")
            if "{{PROJECT_NAME}}" in content:
                fail(f"Placeholder not replaced in {fpath}")
            if project_name not in content:
                fail(f"Project name not injected in {fpath}")

        # Validate expected git commands were invoked with correct working directories
        def called_with(prefix_args, cwd_endswith):
            for call in captured["calls"]:
                args = call["args"]
                cwd = call["cwd"] or ""
                if args[:len(prefix_args)] == prefix_args and cwd.endswith(cwd_endswith):
                    return True
            return False

        child_cwd_suffix = str(Path("projects") / project_name)
        root_cwd_suffix = str(repo_root)

        if not called_with(["git", "init"], child_cwd_suffix):
            fail("git init not called in child project directory")
        if not called_with(["git", "add", "."], child_cwd_suffix):
            fail("git add . not called in child project directory")
        if not called_with(["git", "commit", "-m", "Initial commit"], child_cwd_suffix):
            fail("git commit not called in child project directory with expected message")

        # Check submodule add: last arg should be projects/{project_name} and cwd should be repo root
        submodule_calls = [c for c in captured["calls"] if c["args"][:3] == ["git", "submodule", "add"]]
        if not submodule_calls:
            fail("git submodule add was not invoked")
        ok_sub = False
        for c in submodule_calls:
            args = c["args"]
            cwd = c["cwd"] or ""
            if args[-1] == f"projects/{project_name}" and cwd == str(repo_root):
                ok_sub = True
                break
        if not ok_sub:
            fail("git submodule add did not use expected destination or working directory")

        pass_msg("Child project initialization script meets acceptance criteria.")

    finally:
        # Cleanup and restore
        pm.subprocess.run = original_run
        if target_dir.exists():
            shutil.rmtree(target_dir)


if __name__ == "__main__":
    run()
