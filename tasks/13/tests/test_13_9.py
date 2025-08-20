import os, sys, json, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))


def read(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def fail(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)


def ok(msg):
    print(f"PASS: {msg}")
    sys.exit(0)


def main():
    # 1) Tooling: update_feature_status exists and orchestrator exposes it
    tu_path = os.path.join(ROOT, 'scripts', 'tools', 'task_utils.py')
    if not os.path.exists(tu_path):
        fail('scripts/tools/task_utils.py does not exist')
    tu = read(tu_path)
    if 'def update_feature_status' not in tu:
        fail('update_feature_status function missing in task_utils.py')

    rla_path = os.path.join(ROOT, 'scripts', 'run_local_agent.py')
    if not os.path.exists(rla_path):
        fail('scripts/run_local_agent.py missing')
    rla = read(rla_path)
    if 'def update_feature_status(self, task_id' not in rla:
        fail('AgentTools.update_feature_status not exposed in run_local_agent.py')

    # 2) Docs updated: PLAN_SPECIFICATION.md mentions LLM-friendly Markdown
    plan_spec_path = os.path.join(ROOT, 'docs', 'PLAN_SPECIFICATION.md')
    ps = read(plan_spec_path)
    if 'LLM-Friendly' not in ps and 'LLM friendly' not in ps:
        fail('PLAN_SPECIFICATION.md must mention LLM-friendly plans')
    if 'Markdown' not in ps:
        fail('PLAN_SPECIFICATION.md must state plans are in Markdown')

    # 3) FEATURE_FORMAT.md requires plan field and LLM-friendly Markdown
    ff_path = os.path.join(ROOT, 'docs', 'FEATURE_FORMAT.md')
    if not os.path.exists(ff_path):
        fail('docs/FEATURE_FORMAT.md missing')
    ff = read(ff_path)
    if 'plan' not in ff or 'LLM' not in ff or 'Markdown' not in ff:
        fail('FEATURE_FORMAT.md must document plan field and LLM-friendly Markdown requirements')

    # 4) FILE_ORGANISATION.md: no plan.md, reference embedded plans
    fo_path = os.path.join(ROOT, 'docs', 'FILE_ORGANISATION.md')
    if not os.path.exists(fo_path):
        fail('docs/FILE_ORGANISATION.md missing')
    fo = read(fo_path)
    if 'plan.md' in fo:
        fail('FILE_ORGANISATION.md should not reference plan.md')
    if 'task.json' not in fo or 'plans' not in fo:
        fail('FILE_ORGANISATION.md should state plans are embedded in task.json')

    ok('Feature 13.9: tooling and docs updated for LLM-friendly Markdown plans, and update_feature_status tool exposed.')


if __name__ == '__main__':
    main()
