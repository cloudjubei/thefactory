#!/usr/bin/env python3
import argparse
import os
import re
import sys
from pathlib import Path
import subprocess
from typing import List, Dict, Optional

ROOT = Path(__file__).resolve().parents[1]
TASKS_MD = ROOT / "tasks" / "TASKS.md"

TASK_LINE_RE = re.compile(r"^(\d+)\)\s+([+\-~\?/=])\s+(.*)")
FEATURE_LINE_RE = re.compile(r"^(\d+)\.(\d+)\)\s+([+\-~\?/=])\s+(.*)")


def parse_tasks(tasks_path: Path) -> List[Dict]:
    tasks = []
    if not tasks_path.exists():
        return tasks
    with tasks_path.open("r", encoding="utf-8") as f:
        for line in f:
            m = TASK_LINE_RE.match(line.strip())
            if m:
                tid = int(m.group(1))
                status = m.group(2)
                title = m.group(3).strip()
                tasks.append({"id": tid, "status": status, "title": title})
    return tasks


def plan_path_for_task(task_id: int) -> Path:
    return ROOT / "tasks" / str(task_id) / f"plan_{task_id}.md"


def tests_dir_for_task(task_id: int) -> Path:
    return ROOT / "tasks" / str(task_id) / "tests"


def has_any_tests(task_id: int) -> bool:
    tdir = tests_dir_for_task(task_id)
    if not tdir.exists() or not tdir.is_dir():
        return False
    return any(p.suffix == ".py" for p in tdir.iterdir() if p.is_file())


def parse_features(plan_path: Path) -> List[Dict]:
    feats = []
    if not plan_path.exists():
        return feats
    with plan_path.open("r", encoding="utf-8") as f:
        for line in f:
            m = FEATURE_LINE_RE.match(line.strip())
            if m:
                task_id = int(m.group(1))
                num = int(m.group(2))
                status = m.group(3)
                title = m.group(4).strip()
                feats.append({
                    "task_id": task_id,
                    "number": num,
                    "status": status,
                    "title": title,
                })
    return feats


def ensure_parents(p: Path):
    p.parent.mkdir(parents=True, exist_ok=True)


PLAN_TEMPLATE = """# Plan for Task {task_id}: {title}

## Intent
Create/complete the deliverables for Task {task_id} in compliance with PLAN_SPECIFICATION and FEATURE_FORMAT.

## Context
- tasks/TASKS.md
- docs/PLAN_SPECIFICATION.md
- docs/FEATURE_FORMAT.md
- docs/TESTING.md

## Features
{task_id}.1) - Draft the primary deliverable(s)
   Action: Create the main artifact(s) for this task per TASKS.md acceptance.
   Acceptance: Artifact(s) exist and meet the acceptance criteria.
   Context: docs/PLAN_SPECIFICATION.md, docs/FEATURE_FORMAT.md
   Output: Key files for the task

{task_id}.2) - Write tests for the deliverable(s)
   Action: Create tests under tasks/{task_id}/tests/ that validate acceptance criteria.
   Acceptance: Tests exist and pass.
   Context: docs/TESTING.md, docs/PLAN_SPECIFICATION.md
   Output: tasks/{task_id}/tests/test_{task_id}_1.py (or similar)

{task_id}.3) - Finalize task status and submit
   Action: Update tasks/TASKS.md for this task, submit for review.
   Acceptance: TASKS.md updated; submission completed.
   Context: docs/PLAN_SPECIFICATION.md

## Execution Steps
- Implement each feature atomically, write tests, run tests, then finish_feature.
- After all features pass, update TASKS.md, submit_for_review, finish.
"""


def persona_manager(task_id: Optional[int]):
    tasks = parse_tasks(TASKS_MD)
    print("Manager report:")
    to_check = [t for t in tasks if (task_id is None or t["id"] == task_id)]
    if not to_check:
        print("- No matching tasks.")
        return 0
    missing_plans = []
    for t in to_check:
        p = plan_path_for_task(t["id"])
        if not p.exists():
            missing_plans.append(t)
    print(f"- Total tasks checked: {len(to_check)}")
    print(f"- Tasks missing plan files: {len(missing_plans)}")
    for t in missing_plans:
        print(f"  - Task {t['id']}: {t['title']} (expected {plan_path_for_task(t['id']).relative_to(ROOT)})")
    if not missing_plans:
        print("- All tasks have plan files.")
    return 0


def persona_planner(task_id: Optional[int], apply: bool):
    tasks = parse_tasks(TASKS_MD)
    print("Planner report:")
    to_check = [t for t in tasks if (task_id is None or t["id"] == task_id)]
    if not to_check:
        print("- No matching tasks.")
        return 0
    for t in to_check:
        p = plan_path_for_task(t["id"])
        if p.exists():
            print(f"- Plan exists for Task {t['id']}: {p.relative_to(ROOT)}")
        else:
            print(f"- Missing plan for Task {t['id']}: {t['title']}")
            if apply:
                ensure_parents(p)
                p.write_text(PLAN_TEMPLATE.format(task_id=t["id"], title=t["title"]), encoding="utf-8")
                print(f"  > Created {p.relative_to(ROOT)}")
            else:
                print(f"  > Suggest creating {p.relative_to(ROOT)} (use --apply to scaffold)")
    return 0


def persona_tester(task_id: Optional[int], apply: bool):
    tasks = parse_tasks(TASKS_MD)
    print("Tester report:")
    to_check = [t for t in tasks if (task_id is None or t["id"] == task_id)]
    if not to_check:
        print("- No matching tasks.")
        return 0
    for t in to_check:
        tid = t["id"]
        has_tests = has_any_tests(tid)
        tdir = tests_dir_for_task(tid)
        if has_tests:
            print(f"- Tests found for Task {tid}: {tdir.relative_to(ROOT)}")
        else:
            print(f"- No tests for Task {tid}. Expected directory: {tdir.relative_to(ROOT)}")
            if apply:
                ensure_parents(tdir / "placeholder.txt")
                sample = (
                    "import os, sys\n\n" \
                    "def run():\n" \
                    f"    path = 'tasks/{tid}/tests'\n" \
                    "    ok = os.path.exists(path)\n" \
                    "    print('PASS' if ok else 'FAIL')\n" \
                    "    sys.exit(0 if ok else 1)\n\n" \
                    "if __name__ == '__main__':\n" \
                    "    run()\n"
                )
                test_path = tdir / f"test_{tid}_placeholder.py"
                test_path.write_text(sample, encoding="utf-8")
                print(f"  > Scaffolding test created: {test_path.relative_to(ROOT)}")
            else:
                print("  > Suggest creating tests per docs/TESTING.md (use --apply to scaffold a placeholder)")
    return 0


def persona_developer(task_id: Optional[int]):
    tasks = parse_tasks(TASKS_MD)
    print("Developer report:")
    to_check = [t for t in tasks if (task_id is None or t["id"] == task_id)]
    if not to_check:
        print("- No matching tasks.")
        return 0
    for t in to_check:
        p = plan_path_for_task(t["id"])
        if not p.exists():
            print(f"- Task {t['id']} missing plan; cannot enumerate features. See planner.")
            continue
        feats = parse_features(p)
        pending = [f for f in feats if f["status"] == "-"]
        in_prog = [f for f in feats if f["status"] == "~"]
        unknown = [f for f in feats if f["status"] == "?"]
        print(f"- Task {t['id']} features: total={len(feats)}, pending={len(pending)}, in_progress={len(in_prog)}, unknown={len(unknown)}")
        for f in pending[:5]:  # show up to 5
            print(f"  - Pending: {t['id']}.{f['number']} {f['title']}")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Run repository persona checks/scaffolding (manager, planner, tester, developer).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--persona", required=True, choices=["manager", "planner", "tester", "developer"], help="Persona to run")
    parser.add_argument("--task-id", type=int, default=None, help="Optional specific task ID to focus on")
    parser.add_argument("--apply", action="store_true", help="Apply scaffolding changes when supported (planner, tester)")
    args = parser.parse_args()

    if not TASKS_MD.exists():
        print(f"ERROR: Cannot find {TASKS_MD}")
        return 1

    if args.persona == "manager":
        return persona_manager(args.task_id)
    elif args.persona == "planner":
        return persona_planner(args.task_id, args.apply)
    elif args.persona == "tester":
        return persona_tester(args.task_id, args.apply)
    elif args.persona == "developer":
        return persona_developer(args.task_id)
    else:
        print("Unknown persona.")
        return 2


if __name__ == "__main__":
    sys.exit(main())
