import os
import re
from pathlib import Path

ROOT = Path('.')
DOCKERFILE = ROOT / 'projects' / 'docker' / 'Dockerfile'
README = ROOT / 'projects' / 'docker' / 'RUNNING_DOCKER_README.md'
BUILD_SCRIPT = ROOT / 'projects' / 'docker' / 'build_docker.sh'


def read_text(p: Path) -> str:
    assert p.exists(), f"Expected file to exist: {p}"
    return p.read_text(encoding='utf-8')


def test_dockerfile_exists_and_has_base_python_and_workdir_and_copy_and_deps_and_entrypoint():
    content = read_text(DOCKERFILE)
    lc = content.lower()

    # Base image uses python
    assert re.search(r"^\s*from\s+[^\n]*python", content, re.IGNORECASE | re.MULTILINE), \
        "Dockerfile must use a Python base image (FROM ...python...)."

    # WORKDIR
    assert re.search(r"^\s*workdir\s+", content, re.IGNORECASE | re.MULTILINE), \
        "Dockerfile must set a WORKDIR."

    # COPY project files and dependency manifest
    assert re.search(r"^\s*copy\s+", content, re.IGNORECASE | re.MULTILINE), \
        "Dockerfile must copy files using COPY."

    # Installs dependencies: pip install -r requirements.txt or pip install . or poetry install
    installs_deps = (
        'pip install -r' in lc or
        'pip3 install -r' in lc or
        re.search(r"pip\s+install\s+\.", lc) or
        'poetry install' in lc
    )
    assert installs_deps, "Dockerfile must install dependencies (pip install -r, pip install ., or poetry install)."

    # ENTRYPOINT or CMD present
    has_entry_or_cmd = re.search(r"^\s*(entrypoint|cmd)\s+", content, re.IGNORECASE | re.MULTILINE)
    assert has_entry_or_cmd, "Dockerfile must define an ENTRYPOINT or CMD."

    # Periodic execution evidence: either while true loop/sleep, or cron, or refers to entrypoint.sh with loop/cron
    periodic_in_dockerfile = ('while true' in lc and 'sleep' in lc) or ('cron' in lc)

    entrypoint_refs = re.findall(r"entrypoint[^\n]*\.sh", lc)
    if periodic_in_dockerfile:
        assert True
    elif entrypoint_refs:
        # Try to locate an entrypoint script in repository
        candidate_paths = [
            ROOT / 'projects' / 'docker' / 'entrypoint.sh',
            ROOT / 'entrypoint.sh',
            ROOT / 'scripts' / 'entrypoint.sh'
        ]
        ep_found = False
        ep_periodic = False
        for ep in candidate_paths:
            if ep.exists():
                ep_found = True
                epc = ep.read_text(encoding='utf-8').lower()
                if ('while true' in epc and 'sleep' in epc) or ('cron' in epc):
                    ep_periodic = True
                    break
        assert ep_found, "Dockerfile references an entrypoint script, but no common entrypoint.sh file was found in the repo."
        assert ep_periodic, "Entrypoint script must implement periodic execution (loop+sleep or cron)."
    else:
        assert False, (
            "Dockerfile must establish periodic execution: either inline a loop (while true + sleep), "
            "use cron, or reference an entrypoint script that does."
        )


def test_build_script_exists_and_is_bash_and_handles_env_and_builds_and_guides_run():
    content = read_text(BUILD_SCRIPT)
    lc = content.lower()

    # Bash shebang
    first_line = content.splitlines()[0] if content.splitlines() else ''
    assert first_line.startswith('#!') and 'bash' in first_line.lower(), "build_docker.sh must start with a bash shebang."

    # Clones repository
    assert 'git clone' in lc, "build_docker.sh must clone the repository (git clone)."

    # Checks for .env presence
    assert '.env' in content, "build_docker.sh must reference a .env file (checking existence or usage)."

    # Builds Docker image with Dockerfile path and a tag
    assert 'docker build' in lc, "build_docker.sh must build the Docker image (docker build)."
    assert '-f projects/docker/dockerfile' in lc, "build_docker.sh must use the Dockerfile at projects/docker/Dockerfile (-f projects/docker/Dockerfile)."
    assert re.search(r"\-t\s+[-\w:.]+", content), "build_docker.sh should tag the image using -t."

    # Provides run instructions that include passing env via --env-file or mounting .env
    has_run = 'docker run' in lc
    has_env_provision = ('--env-file' in lc) or re.search(r"\-v\s+[^\n]*\.env", lc)
    assert has_run and has_env_provision, (
        "build_docker.sh must provide instructions to run the container and supply env via --env-file or volume mounting .env"
    )


def test_readme_exists_and_instructions_for_env_build_run_and_periodic():
    content = read_text(README)
    lc = content.lower()

    # Mentions .env and API keys
    assert '.env' in lc and 'api' in lc, "README must explain preparing a .env with API keys."

    # Mentions build script and/or docker build command
    mentions_build_script = 'build_docker.sh' in lc
    mentions_docker_build = 'docker build' in lc and 'projects/docker/dockerfile' in lc
    assert mentions_build_script or mentions_docker_build, "README must explain how to build the Docker image (build script or docker build)."

    # Mentions docker run with env provisioning
    assert 'docker run' in lc, "README must provide docker run instructions."
    assert ('--env-file' in lc) or ('.env' in lc and ('-v' in lc or 'volume' in lc)), \
        "README must show how to provide env to the container (--env-file or volume mount of .env)."

    # Mentions periodic execution inside container (cron or loop/sleep)
    assert ('cron' in lc) or ('periodic' in lc) or ('while true' in lc) or ('sleep' in lc), \
        "README must clarify the agent runs periodically inside the container (cron or loop/sleep)."

    # Clarify no host-level scheduler needed
    hint_no_host_sched = ('inside the container' in lc) or ('without affecting the host' in lc) or ('no host' in lc)
    assert hint_no_host_sched, "README should indicate scheduling happens inside the container, not on host."
