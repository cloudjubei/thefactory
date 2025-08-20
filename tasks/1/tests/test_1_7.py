import sys
import os

def run():
    file_path = "docs/PLAN_SPECIFICATION.md"
    if not os.path.exists(file_path):
        print(f"FAIL: {file_path} does not exist.")
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    acceptance_criteria = {
        "`docs/PLAN_SPECIFICATION.md` exists": True,
        "references `docs/tasks/task_format.py`": "docs/tasks/task_format.py" in content,
        "references `docs/tasks/task_example.json`": "docs/tasks/task_example.json" in content,
        "references `docs/tasks/TASKS_GUIDANCE.md`": "docs/tasks/TASKS_GUIDANCE.md" in content,
        "references `docs/TESTING.md`": "docs/TESTING.md" in content,
        "explains full scope is mandatory": "scope the entire task" in content,
        "explains generic high level plan": "high-level plan" in content,
        "explains step-by-step feature plan": "step-by-step guide" in content,
        "explains rigorous acceptance criteria": "rigorous `acceptance` criteria" in content,
        "explains status update via `write_file`": "`write_file` tool" in content,
        "explains `finish_feature` for features": "`finish_feature` tool" in content,
        "explains `submit_for_review` for task": "`submit_for_review` tool" in content,
    }

    failed_criteria = [key for key, passed in acceptance_criteria.items() if not passed]

    if failed_criteria:
        print(f"FAIL: The following acceptance criteria failed for {file_path}:")
        for criterion in failed_criteria:
            print(f"  - {criterion}")
        sys.exit(1)

    print(f"PASS: {file_path} meets all acceptance criteria.")
    sys.exit(0)

if __name__ == "__main__":
    run()
