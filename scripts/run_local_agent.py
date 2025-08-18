#!/usr/bin/env python3
"""
Agent Orchestrator (scripts/run_local_agent.py)

A simple, non-intelligent executor that:
- Provides project context to the LLM Agent
- Enforces the JSON response contract (docs/TOOL_ARCHITECTURE.md)
- Exposes tool functions and executes them in order
- Supports Single and Continuous execution modes

Providers:
- manual (default): Prints the prompt and asks the user to paste the Agent's JSON plan
- openai: Uses OpenAI SDK if available (requires OPENAI_API_KEY & OPENAI_MODEL)
- http: Calls an OpenAI-compatible API via HTTP (requires OPENAI_API_KEY, OPENAI_MODEL, optional OPENAI_BASE_URL)

Environment variables:
- OPENAI_API_KEY, OPENAI_MODEL, OPENAI_BASE_URL (for http provider)
- GITHUB_TOKEN (optional, for creating PR via GitHub API if gh CLI not available)

This script follows docs/TOOL_ARCHITECTURE.md and docs/AGENT_PRINCIPLES.md.
"""
from __future__ import annotations
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent


# ------------- Utilities -------------

def read_file(rel_path: str) -> str:
    p = (REPO_ROOT / rel_path).resolve()
    if not str(p).startswith(str(REPO_ROOT)):
        raise ValueError(f"Path escapes repo root: {rel_path}")
    return p.read_text(encoding="utf-8")


def ensure_parent_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


# ------------- Provider Implementations -------------

class ManualProvider:
    name = "manual"

    def complete(self, system_prompt: str, user_prompt: str) -> str:
        print("\n===== SYSTEM PROMPT (read-only) =====\n")
        print(system_prompt)
        print("\n===== USER PROMPT (context) =====\n")
        print(user_prompt)
        print("\nPaste the Agent's JSON response below (single line or multi-line). Finish with EOF (Ctrl-D on Unix, Ctrl-Z then Enter on Windows).\n")
        data = sys.stdin.read()
        return data.strip()


class OpenAIProvider:
    name = "openai"

    def __init__(self):
        try:
            import openai  # type: ignore
        except Exception as e:
            raise RuntimeError("openai package not available. Install it or choose provider=manual/http.") from e
        self.openai = openai
        self.client = openai.OpenAI()
        self.model = os.getenv("OPENAI_MODEL") or "gpt-4o-mini"

    def complete(self, system_prompt: str, user_prompt: str) -> str:
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
            response_format={"type": "json_object"},
        )
        return resp.choices[0].message.content or ""


class HTTPProvider:
    name = "http"

    def __init__(self):
        import requests  # lazy import may raise if not installed
        self.requests = requests
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL") or "gpt-4o-mini"
        self.base_url = os.getenv("OPENAI_BASE_URL") or "https://api.openai.com/v1"
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY must be set for http provider")

    def complete(self, system_prompt: str, user_prompt: str) -> str:
        url = f"{self.base_url.rstrip('/')}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.2,
            "response_format": {"type": "json_object"},
        }
        r = self.requests.post(url, headers=headers, data=json.dumps(payload))
        r.raise_for_status()
        data = r.json()
        return data["choices"][0]["message"]["content"]


# ------------- Tools -------------

class AgentTools:
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run

    def write_file(self, path: str, content: str) -> Dict[str, Any]:
        abs_path = (REPO_ROOT / path).resolve()
        if not str(abs_path).startswith(str(REPO_ROOT)):
            raise ValueError(f"write_file path escapes repo root: {path}")
        if self.dry_run:
            return {"ok": True, "message": f"Dry-run: would write {path}", "bytes": len(content)}
        ensure_parent_dir(abs_path)
        abs_path.write_text(content, encoding="utf-8")
        return {"ok": True, "message": f"Wrote {path}", "bytes": len(content)}

    def retrieve_context_files(self, paths: List[str]) -> Dict[str, Any]:
        files: Dict[str, str] = {}
        for p in paths:
            abs_path = (REPO_ROOT / p).resolve()
            if not str(abs_path).startswith(str(REPO_ROOT)):
                raise ValueError(f"retrieve_context_files path escapes repo root: {p}")
            if abs_path.exists():
                files[p] = abs_path.read_text(encoding="utf-8")
            else:
                files[p] = ""
        return {"ok": True, "files": files}

    def rename_files(self, operations: List[Dict[str, str]], overwrite: bool = False, dry_run: bool = False) -> Dict[str, Any]:
        # Delegate to scripts/rename_files.py implementation
        from scripts.rename_files import rename_files as _rename_impl  # type: ignore
        result_json = _rename_impl(operations, overwrite=overwrite, dry_run=dry_run)
        return {"ok": True, "result": json.loads(result_json)}

    def submit_for_review(self, task_id: int, task_title: str) -> Dict[str, Any]:
        # Standardized commit and PR creation
        ts = time.strftime("%Y%m%d-%H%M%S")
        slug = re.sub(r"[^a-z0-9-]+", "-", task_title.lower()).strip("-") or f"task-{task_id}"
        branch = f"task-{task_id}-{slug}-{ts}"
        commit_msg = f"Task {task_id}: {task_title} (auto-submit)"

        def run(cmd: List[str], check: bool = True) -> subprocess.CompletedProcess:
            return subprocess.run(cmd, cwd=str(REPO_ROOT), check=check, capture_output=True, text=True)

        if self.dry_run:
            return {"ok": True, "message": f"Dry-run: would commit and open PR on branch {branch}"}

        try:
            run(["git", "add", "-A"]) 
            # Allow empty commits to standardize flow
            run(["git", "commit", "-m", commit_msg, "--allow-empty"]) 
            run(["git", "checkout", "-b", branch])
            run(["git", "push", "-u", "origin", branch])
        except subprocess.CalledProcessError as e:
            return {"ok": False, "message": f"Git operation failed: {e.stderr or e.stdout}"}

        # Try GitHub CLI first
        pr_url = None
        if shutil.which("gh"):
            try:
                cp = run(["gh", "pr", "create", "--fill", "--head", branch])
                pr_url = cp.stdout.strip() or None
            except subprocess.CalledProcessError:
                pr_url = None
        else:
            # Fallback: Best-effort GitHub API if GITHUB_TOKEN and origin URL are available
            token = os.getenv("GITHUB_TOKEN")
            try:
                origin = run(["git", "config", "--get", "remote.origin.url"]).stdout.strip()
            except subprocess.CalledProcessError:
                origin = ""
            if token and origin:
                try:
                    import requests  # type: ignore
                    m = re.search(r"[:/]([^/]+)/([^/.]+)(?:\.git)?$", origin)
                    if m:
                        owner, repo = m.group(1), m.group(2)
                        api_url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
                        base_branch = os.getenv("BASE_BRANCH", "main")
                        payload = {"title": commit_msg, "head": branch, "base": base_branch, "body": "Automated submission by Orchestrator."}
                        r = requests.post(api_url, headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}, json=payload)
                        if r.ok:
                            pr_url = r.json().get("html_url")
                except Exception:
                    pr_url = None

        return {"ok": True, "branch": branch, "pr_url": pr_url}

    def ask_question(self, question_text: str) -> Dict[str, Any]:
        print("\n=== QUESTION FROM AGENT ===\n" + question_text + "\n")
        # Halts execution as per spec
        sys.exit(0)

    def finish(self, reason: Optional[str] = None) -> Dict[str, Any]:
        if reason:
            print(f"finish: {reason}")
        # Signal completion of this cycle
        sys.exit(0)


# ------------- Orchestrator Core -------------

@dataclass
class Plan:
    plan: str
    tool_calls: List[Dict[str, Any]]


def validate_plan(obj: Any) -> Plan:
    if not isinstance(obj, dict):
        raise ValueError("Agent output must be a JSON object")
    if "plan" not in obj or "tool_calls" not in obj:
        raise ValueError("JSON must contain 'plan' and 'tool_calls'")
    if not isinstance(obj["plan"], str):
        raise ValueError("'plan' must be a string")
    if not isinstance(obj["tool_calls"], list):
        raise ValueError("'tool_calls' must be a list")
    for i, call in enumerate(obj["tool_calls" ]):
        if not isinstance(call, dict):
            raise ValueError(f"tool_calls[{i}] must be an object")
        if "tool_name" not in call or "arguments" not in call:
            raise ValueError(f"tool_calls[{i}] must contain 'tool_name' and 'arguments'")
    return Plan(plan=obj["plan"], tool_calls=obj["tool_calls"])


def build_system_prompt() -> str:
    schema = {
        "type": "object",
        "properties": {
            "plan": {"type": "string"},
            "tool_calls": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "tool_name": {"type": "string"},
                        "arguments": {"type": "object"}
                    },
                    "required": ["tool_name", "arguments"]
                }
            }
        },
        "required": ["plan", "tool_calls"]
    }
    return (
        "You are the Agent. You must respond with a SINGLE JSON object that includes 'plan' and 'tool_calls'.\n"
        "Follow docs/AGENT_PRINCIPLES.md and docs/TOOL_ARCHITECTURE.md.\n"
        "Only use the available tools. Do not include any other fields.\n"
        f"JSON Schema (for reference): {json.dumps(schema)}\n"
    )


def build_user_prompt() -> str:
    # Provide the minimal core context files
    context_files = [
        "tasks/TASKS.md",
        "docs/TOOL_ARCHITECTURE.md",
        "docs/AGENT_PRINCIPLES.md",
        "docs/TASK_FORMAT.md",
        "docs/PLAN_SPECIFICATION.md",
        "docs/FEATURE_FORMAT.md",
        "docs/SPEC.md",
        "docs/SPECIFICATION_GUIDE.md",
        "docs/FILE_ORGANISATION.md",
    ]
    parts = []
    for f in context_files:
        p = (REPO_ROOT / f)
        if p.exists():
            parts.append(f"--- START {f} ---\n{p.read_text(encoding='utf-8')}\n--- END {f} ---\n")
    return "\n".join(parts)


def get_provider(name: str):
    name = name.lower()
    if name == "manual":
        return ManualProvider()
    if name == "openai":
        return OpenAIProvider()
    if name == "http":
        return HTTPProvider()
    raise ValueError(f"Unknown provider: {name}")


def execute_plan(plan_obj: Plan, tools: AgentTools) -> None:
    tool_map = {
        "write_file": tools.write_file,
        "retrieve_context_files": tools.retrieve_context_files,
        "rename_files": tools.rename_files,
        "submit_for_review": tools.submit_for_review,
        "ask_question": tools.ask_question,
        "finish": tools.finish,
    }

    print("\n=== Agent Plan ===\n" + plan_obj.plan + "\n")

    for i, call in enumerate(plan_obj.tool_calls, start=1):
        tname = call.get("tool_name")
        args = call.get("arguments", {})
        if tname not in tool_map:
            raise ValueError(f"Unknown tool: {tname}")
        fn = tool_map[tname]
        print(f"[Tool {i}] {tname} args={json.dumps(args)[:500]}")
        result = fn(**args)
        # Print small result summary to help debugging
        try:
            snippet = json.dumps(result)
        except Exception:
            snippet = str(result)
        print(f"[Tool {i}] result={snippet[:800]}")


def run_once(provider_name: str, dry_run: bool = False) -> None:
    provider = get_provider(provider_name)
    system_prompt = build_system_prompt()
    user_prompt = build_user_prompt()
    raw = provider.complete(system_prompt, user_prompt)

    try:
        obj = json.loads(raw)
    except Exception as e:
        raise ValueError(f"Agent response is not valid JSON: {e}\nRaw: {raw[:1000]}")

    plan = validate_plan(obj)
    tools = AgentTools(dry_run=dry_run)
    execute_plan(plan, tools)


def continuous_loop(provider_name: str, dry_run: bool = False) -> None:
    while True:
        try:
            run_once(provider_name, dry_run=dry_run)
        except SystemExit:
            # finish() or ask_question() halts; exit loop
            break
        except Exception as e:
            print(f"Error during cycle: {e}")
            break
        # Pull latest before next iteration (best-effort)
        try:
            subprocess.run(["git", "fetch", "origin"], cwd=str(REPO_ROOT), check=False)
            subprocess.run(["git", "pull"], cwd=str(REPO_ROOT), check=False)
        except Exception:
            pass


def main():
    parser = argparse.ArgumentParser(description="Agent Orchestrator")
    parser.add_argument("--provider", default=os.getenv("PROVIDER", "manual"), choices=["manual", "openai", "http"], help="LLM provider")
    parser.add_argument("--mode", default=os.getenv("MODE", "single"), choices=["single", "continuous"], help="Execution mode")
    parser.add_argument("--dry-run", action="store_true", help="Do not modify files or create PRs")
    args = parser.parse_args()

    if args.mode == "single":
        run_once(args.provider, dry_run=args.dry_run)
    else:
        continuous_loop(args.provider, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
