import os
import sys


def read_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f'FAIL: Could not read {path}: {e}')
        sys.exit(1)


def verify_headings(content, required):
    missing = [h for h in required if h not in content]
    return missing


def run_test():
    guide_path = 'docs/SPECIFICATION_GUIDE.md'
    template_path = 'docs/TEMPLATE.md'

    required_headings = [
        '# Problem Statement',
        '# Inputs and Outputs',
        '# Constraints',
        '# Success Criteria',
        '# Edge Cases',
        '# Examples',
    ]

    # 1) Existence checks
    missing_files = []
    for p in (guide_path, template_path):
        if not os.path.exists(p):
            missing_files.append(p)
    if missing_files:
        print('FAIL: Missing files: ' + ', '.join(missing_files))
        sys.exit(1)

    # 2) Content checks for required headings
    guide_content = read_file(guide_path)
    template_content = read_file(template_path)

    guide_missing = verify_headings(guide_content, required_headings)
    template_missing = verify_headings(template_content, required_headings)

    msgs = []
    if guide_missing:
        msgs.append(f"{guide_path} missing: {', '.join(guide_missing)}")
    if template_missing:
        msgs.append(f"{template_path} missing: {', '.join(template_missing)}")

    if msgs:
        print('FAIL: ' + ' | '.join(msgs))
        sys.exit(1)

    print('PASS: SPECIFICATION_GUIDE.md and TEMPLATE.md exist and contain all required headings.')
    sys.exit(0)


if __name__ == '__main__':
    run_test()
