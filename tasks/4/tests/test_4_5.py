import os
import stat

DOC_PATH = os.path.join('docs', 'DOCKER_SETUP.md')
RUN_SH_PATH = os.path.join('scripts', 'docker', 'run.sh')

def test_docker_setup_doc_exists():
    assert os.path.isfile(DOC_PATH), f"Missing {DOC_PATH}"

def test_docker_setup_doc_content():
    with open(DOC_PATH, 'r', encoding='utf-8') as f:
        text = f.read()
    # Prerequisites
    assert 'Prerequisites' in text or 'Requirements' in text, "Doc should have a Prerequisites/Requirements section"
    assert 'Docker' in text, "Doc should mention Docker"
    assert 'Docker Compose' in text or 'docker-compose' in text or 'docker compose' in text, "Doc should mention Docker Compose"
    # Usage of run.sh
    assert 'scripts/docker/run.sh' in text, "Doc should reference scripts/docker/run.sh"
    # Arguments passing and example
    assert '--agent' in text, "Doc should show passing --agent to the run script"
    assert '--task' in text, "Doc should show passing --task to the run script"
    # Environment file reuse
    assert '.env' in text, "Doc should mention .env usage/reuse"


def test_run_sh_exists_and_executable():
    assert os.path.isfile(RUN_SH_PATH), f"Missing {RUN_SH_PATH}"
    st = os.stat(RUN_SH_PATH)
    is_exec = bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    assert is_exec, f"{RUN_SH_PATH} must be executable"
