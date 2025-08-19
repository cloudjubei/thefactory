import os
import re
import sys

def run():
    path = "tasks/TASKS.md"
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        content = "".join(lines)

    # Check reference to TASK_FORMAT.md near the top
    top_block = "".join(lines[:10]) if len(lines) >= 10 else "".join(lines)
    if "docs/TASK_FORMAT.md" not in top_block:
        print("FAIL: Top of tasks/TASKS.md does not reference docs/TASK_FORMAT.md.")
        sys.exit(1)

    # Extract task numbering and status codes
    nums = []
    statuses = []
    pattern = re.compile(r"^(\d+)\)\s([+\-~\?=/])\s", re.UNICODE)
    for line in lines:
        m = pattern.match(line)
        if m:
            nums.append(int(m.group(1)))
            statuses.append(m.group(2))

    if not nums:
        print("FAIL: No tasks found in tasks/TASKS.md.")
        sys.exit(1)

    # Check strictly increasing numbering
    for i in range(1, len(nums)):
        if nums[i] <= nums[i-1]:
            print(f"FAIL: Task numbering not strictly increasing at index {i}: {nums[i-1]} -> {nums[i]}.")
            sys.exit(1)

    # Verify all statuses are valid
    valid_status = set(["+", "-", "?", "~", "/", "="])
    invalid = [s for s in statuses if s not in valid_status]
    if invalid:
        print(f"FAIL: Found invalid status codes: {invalid}")
        sys.exit(1)

    print("PASS: TASKS.md references TASK_FORMAT.md and has strictly increasing, well-formed task entries.")
    sys.exit(0)

if __name__ == "__main__":
    run()
