import os
import re
import sys


def run():
    """
    Tests Task 1, Feature 1.2 (Apply format to TASKS).
    Acceptance (encoded):
    - tasks/TASKS.md references docs/TASK_FORMAT.md near the top
    - Each task line follows "N) <status> Title" with status in {+, -, ~, ?, /, =}
    - Task numbering is sequential and ordered (1..N without gaps)
    """
    tasks_path = "tasks/TASKS.md"

    if not os.path.exists(tasks_path):
        print("FAIL: tasks/TASKS.md does not exist.")
        sys.exit(1)

    with open(tasks_path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    head = "\n".join(lines[:10])
    if "TASK_FORMAT.md" not in head:
        print("FAIL: tasks/TASKS.md does not reference docs/TASK_FORMAT.md at the top.")
        sys.exit(1)

    # Extract task lines like: "12) - Plan specification"
    pattern = re.compile(r"^(\d+)\)\s+([+\-~?/=])\s+.+$")
    entries = []
    for line in lines:
        m = pattern.match(line.strip())
        if m:
            entries.append((int(m.group(1)), m.group(2), line.strip()))

    if not entries:
        print("FAIL: No task entries found in tasks/TASKS.md.")
        sys.exit(1)

    # Validate statuses
    allowed_statuses = set(["+", "-", "~", "?", "/", "="])
    bad_status = [(n, s, l) for (n, s, l) in entries if s not in allowed_statuses]
    if bad_status:
        detail = ", ".join([f"{n}) {s}" for n, s, _ in bad_status])
        print(f"FAIL: Found invalid status symbols: {detail}")
        sys.exit(1)

    # Validate numbering: strictly sequential and ordered
    numbers = [n for n, _, _ in entries]
    # ensure no duplicates and sorted order equals original order
    if numbers != sorted(numbers):
        print("FAIL: Task numbering is not in ascending order.")
        sys.exit(1)
    if len(set(numbers)) != len(numbers):
        print("FAIL: Duplicate task numbers detected.")
        sys.exit(1)
    expected = list(range(1, max(numbers) + 1))
    if numbers != expected:
        print(f"FAIL: Task numbers are not sequential 1..{max(numbers)} without gaps. Found: {numbers}")
        sys.exit(1)

    print("PASS: tasks/TASKS.md references the format and tasks follow structure and status codes.")
    sys.exit(0)


if __name__ == "__main__":
    run()
