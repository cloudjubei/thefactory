import os, sys


def read(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def run():
    guidance_path = 'docs/tasks/TASKS_GUIDANCE.md'
    if not os.path.exists(guidance_path):
        print(f'FAIL: {guidance_path} does not exist.')
        sys.exit(1)
    content = read(guidance_path)
    required_phrases = [
        '# Task Authoring Guidance',
        'tasks/{task_id}/task.json',
        'docs/tasks/task_format.py',
        'JSON-based',
    ]
    missing = [s for s in required_phrases if s not in content]
    if missing:
        print('FAIL: Guidance file missing phrases: ' + ', '.join(missing))
        sys.exit(1)

    legacy1 = 'docs/TASK_FORMAT.md'
    legacy2 = 'docs/FEATURE_FORMAT.md'
    legacy_present = [p for p in [legacy1, legacy2] if os.path.exists(p)]
    if legacy_present:
        print('FAIL: Legacy files still present: ' + ', '.join(legacy_present))
        sys.exit(1)

    print('PASS: TASKS_GUIDANCE.md exists with JSON-based guidance and legacy files are removed.')
    sys.exit(0)


if __name__ == '__main__':
    run()
