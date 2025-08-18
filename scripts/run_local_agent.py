#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_local_agent.py

A minimal orchestrator that executes the Agent's JSON plan by invoking local tools.
This update adds support for running a specific task (-t) and an optional feature (-f),
and ensures the submit_for_review tool creates an appropriate branch name:
- tasks/{task_id}
- features/{task_id}_{feature_id}

It adheres to the contracts in docs/AGENT_PRINCIPLES.md and docs/TOOL_ARCHITECTURE.md.

Usage examples:
  python scripts/run_local_agent.py -t 15 < agent_plan.json
  python scripts/run_local_agent.py -t 15 -f 1 < agent_plan.json

If no JSON is piped to stdin, the script will wait for input and then exit gracefully.
"""
import argparse
import json
import os
import sys
import subprocess
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional

REPO_ROOT = Path(__file__).resolve().parents[1]

class AgentError(Exception):
    pass

class AgentTools:
    @staticmethod
    def write_file(path: str, content: str) -> Dict[str, Any]:
        abs_path = REPO_ROOT / path
        abs_path.parent.mkdir(parents=True, exist_ok=True)
        abs_path.write_text(content, encoding='utf-8')
        return {"ok": True, "path": path, "bytes": len(content.encode('utf-8'))}

    @staticmethod
    def retrieve_context_files(paths: List[str]) -> Dict[str, Any]:
        results = {}
        for p in paths:
            abs_path = REPO_ROOT / p
            if abs_path.exists() and abs_path.is_file():
                results[p] = abs_path.read_text(encoding='utf-8')
            else:
                results[p] = None
        return {"ok": True, "files": results}

    @staticmethod
    def rename_files(operations: List[Dict[str, str]], overwrite: bool = False, dry_run: bool = False) -> str:
        summary = {"moved": 0, "skipped": 0, "errors": 0}
        results = []
        try:
            for op in operations:
                src = (REPO_ROOT / op.get("from_path", "")).resolve()
                dst = (REPO_ROOT / op.get("to_path", "")).resolve()
                # Prevent escaping repo
                if REPO_ROOT not in src.parents or REPO_ROOT not in dst.parents:
                    results.append({"status": "error", "message": "Operation outside repo is not allowed", "from": str(src), "to": str(dst)})
                    summary["errors"] += 1
                    continue
                if dry_run:
                    results.append({"status": "dry_run", "message": "Validated", "from": str(src.relative_to(REPO_ROOT)), "to": str(dst.relative_to(REPO_ROOT))})
                    continue
                if dst.exists():
                    if not overwrite:
                        results.append({"status": "skipped", "message": "Destination exists", "from": str(src), "to": str(dst)})
                        summary["skipped"] += 1
                        continue
                    if dst.is_file():
                        dst.unlink()
                    else:
                        shutil.rmtree(dst)
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(src), str(dst))
                results.append({"status": "moved", "from": str(src.relative_to(REPO_ROOT)), "to": str(dst.relative_to(REPO_ROOT))})
                summary["moved"] += 1
            ok = summary["errors"] == 0
            return json.dumps({"ok": ok, "summary": summary, "results": results}, indent=2)
        except Exception as e:
            return json.dumps({"ok": False, "summary": summary, "results": results, "error": str(e)})

    @staticmethod
    def _run_cmd(cmd: List[str], check: bool = True) -> subprocess.CompletedProcess:
        return subprocess.run(cmd, cwd=REPO_ROOT, check=check, capture_output=True, text=True)

    @staticmethod
    def _git_repo_exists() -> bool:
        try:
            AgentTools._run_cmd(["git", "rev-parse", "--is-inside-work-tree"])  # type: ignore[arg-type]
            return True
        except Exception:
            return False

    @staticmethod
    def _git_branch_exists(branch: str) -> bool:
        try:
            AgentTools._run_cmd(["git", "show-ref", "--verify", f"refs/heads/{branch}"])
            return True
        except Exception:
            return False

    @staticmethod
    def _remote_exists(name: str = "origin") -> bool:
        try:
            AgentTools._run_cmd(["git", "remote", "get-url", name])
            return True
        except Exception:
            return False

    @staticmethod
    def _gh_exists() -> bool:
        return shutil.which("gh") is not None

    @staticmethod
    def _compute_branch_name(task_id: Optional[int], task_title: Optional[str]) -> str:
        # Prefer runtime selection via env (set by -t/-f)
        sel_task = os.environ.get("SELECTED_TASK_ID")
        sel_feat = os.environ.get("SELECTED_FEATURE_ID")
        if sel_task and sel_feat:
            return f"features/{sel_task}_{sel_feat}"
        if sel_task:
            return f"tasks/{sel_task}"
        # Fallback to provided task_id if env not set
        if task_id is not None:
            return f"tasks/{task_id}"
        # Ultimate fallback
        safe_title = (task_title or "change").strip().lower().replace(" ", "-")
        return f"tasks/unspecified-{safe_title[:30]}"

    @staticmethod
    def submit_for_review(task_id: int, task_title: str) -> Dict[str, Any]:
        if not AgentTools._git_repo_exists():
            return {"ok": False, "error": "Not a git repository. Initialize git to use submit_for_review."}
        branch = AgentTools._compute_branch_name(task_id, task_title)
        # Create/switch branch
        try:
            AgentTools._run_cmd(["git", "checkout", "-B", branch])
        except subprocess.CalledProcessError as e:
            return {"ok": False, "error": f"Failed to create/switch branch {branch}: {e.stderr}"}
        # Stage all changes
        try:
            AgentTools._run_cmd(["git", "add", "-A"]) 
        except subprocess.CalledProcessError as e:
            return {"ok": False, "error": f"git add failed: {e.stderr}"}
        # Commit (allow empty to ensure branch exists with a commit)
        msg = f"Task {task_id}: {task_title} - automated submission"
        try:
            AgentTools._run_cmd(["git", "commit", "--allow-empty", "-m", msg])
        except subprocess.CalledProcessError as e:
            return {"ok": False, "error": f"git commit failed: {e.stderr}"}
        # Push if remote exists
        pushed = False
        pr_url = None
        if AgentTools._remote_exists("origin"):
            try:
                AgentTools._run_cmd(["git", "push", "-u", "origin", branch])
                pushed = True
            except subprocess.CalledProcessError as e:
                # Non-fatal: still return ok with message
                pushed = False
        # Create PR if gh is available and we pushed
        if pushed and AgentTools._gh_exists():
            try:
                # Use --fill to auto-fill body from commits, override title
                pr = AgentTools._run_cmd([
                    "gh", "pr", "create",
                    "--title", msg,
                    "--body", f"Automated submission for task {task_id}: {task_title}"
                ], check=True)
                pr_url = pr.stdout.strip()
            except subprocess.CalledProcessError:
                pr_url = None
        return {"ok": True, "branch": branch, "pushed": pushed, "pr_url": pr_url}

    @staticmethod
    def ask_question(question_text: str) -> Dict[str, Any]:
        print("ASK_QUESTION:")
        print(question_text)
        # In interactive orchestrations, this would halt the loop.
        return {"ok": True, "question": question_text}

    @staticmethod
    def finish(reason: Optional[str] = None) -> Dict[str, Any]:
        if reason:
            print(f"FINISH: {reason}")
        else:
            print("FINISH")
        return {"ok": True, "reason": reason}


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the local Agent Orchestrator.")
    parser.add_argument("--task", "-t", type=int, help="Task ID to execute", required=False)
    parser.add_argument("--feature", "-f", type=str, help="Feature ID to execute (requires -t)", required=False)
    parser.add_argument("--input", "-i", type=str, help="Path to a JSON file containing the agent plan (optional). If not provided, stdin is used.", required=False)
    return parser.parse_args(argv)


def load_plan_from_input(input_path: Optional[str]) -> Optional[Dict[str, Any]]:
    try:
        if input_path:
            data = Path(input_path).read_text(encoding='utf-8')
        else:
            if sys.stdin.isatty():
                # No piped input
                return None
            data = sys.stdin.read()
        data = data.strip()
        if not data:
            return None
        return json.loads(data)
    except Exception:
        return None


def execute_plan(plan: Dict[str, Any], selected_task: Optional[int], selected_feature: Optional[str]) -> None:
    # Enforce schema: must have tool_calls list
    tool_calls = plan.get("tool_calls")
    if not isinstance(tool_calls, list):
        raise AgentError("Invalid plan: missing or invalid 'tool_calls' list")

    # Export selection to env so tools can use it (e.g., submit_for_review branch naming)
    if selected_task is not None:
        os.environ["SELECTED_TASK_ID"] = str(selected_task)
    if selected_feature is not None:
        os.environ["SELECTED_FEATURE_ID"] = str(selected_feature)

    for idx, call in enumerate(tool_calls, start=1):
        name = call.get("tool_name")
        args = call.get("arguments", {})
        if name == "write_file":
            AgentTools.write_file(args["path"], args["content"])  # type: ignore[index]
        elif name == "retrieve_context_files":
            AgentTools.retrieve_context_files(args.get("paths", []))
        elif name == "rename_files":
            AgentTools.rename_files(args.get("operations", []), bool(args.get("overwrite", False)), bool(args.get("dry_run", False)))
        elif name == "submit_for_review":
            AgentTools.submit_for_review(int(args.get("task_id")), str(args.get("task_title")))
        elif name == "ask_question":
            AgentTools.ask_question(str(args.get("question_text")))
            # In interactive/continuous mode, this would halt further execution
            break
        elif name == "finish":
            AgentTools.finish(str(args.get("reason", "")))
            break
        else:
            raise AgentError(f"Unknown tool: {name}")


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    if args.feature and not args.task:
        print("Error: --feature/-f requires --task/-t to be set.")
        return 2

    plan = load_plan_from_input(args.input)
    if not plan:
        # No plan provided; in real usage the orchestrator would call the LLM here.
        print("No JSON plan provided on stdin or via --input. Nothing to execute.")
        if args.task:
            print(f"Selection captured: task={args.task}, feature={args.feature or 'N/A'}")
        return 0

    try:
        execute_plan(plan, args.task, args.feature)
        return 0
    except AgentError as e:
        print(f"AgentError: {e}")
        return 1
    except Exception as e:
        print(f"Unhandled error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
