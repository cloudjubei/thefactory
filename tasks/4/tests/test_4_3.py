import os, sys, re


def read_file(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def extract_headings(content: str):
    headings = []
    for line in content.splitlines():
        if re.match(r'^\s*#{1,6}\s+\S', line):
            text = re.sub(r'^\s*#{1,6}\s+', '', line).strip()
            headings.append(text)
    return headings


def run():
    path = 'docs/SPEC.md'
    if not os.path.exists(path):
        print(f"FAIL: {path} does not exist.")
        sys.exit(1)

    content = read_file(path)

    # Check reference to SPECIFICATION_GUIDE at the top (within first 20 non-empty lines)
    non_empty_lines = [ln for ln in content.splitlines() if ln.strip() != '']
    top_block = "\n".join(non_empty_lines[:20])
    if 'docs/SPECIFICATION_GUIDE.md' not in top_block:
        print('FAIL: docs/SPEC.md does not reference docs/SPECIFICATION_GUIDE.md at the top (first ~20 lines).')
        sys.exit(1)

    # Required sections and order
    required = [
        'Problem Statement',
        'Inputs and Outputs',
        'Constraints',
        'Success Criteria',
        'Edge Cases',
        'Examples',
    ]

    headings = extract_headings(content)
    if not headings:
        print('FAIL: No headings found in docs/SPEC.md.')
        sys.exit(1)

    # Allow a single document title heading before the required sequence
    start_index = 0
    if headings and headings[0] != required[0]:
        start_index = 1

    if len(headings) < start_index + len(required):
        print(f"FAIL: Not enough headings for required sections. Found {len(headings)}, need {len(required)} starting at index {start_index}.")
        sys.exit(1)

    block = headings[start_index:start_index + len(required)]
    mismatches = []
    for i, req in enumerate(required):
        if req not in block[i]:
            mismatches.append(f"Expected heading {i+1} to contain '{req}', got '{block[i]}'")

    if mismatches:
        print('FAIL: Section order/names do not match guide:\n- ' + '\n- '.join(mismatches))
        sys.exit(1)

    print('PASS: SPEC.md references SPECIFICATION_GUIDE.md at top and includes required sections in correct order (with no extraneous sections before them beyond an optional title).')
    sys.exit(0)


if __name__ == '__main__':
    run()
