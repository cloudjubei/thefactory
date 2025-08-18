# Plan for Task 11: Running in docker

## Intent
This plan addresses Task 11 by creating the necessary documentation and Docker-related files to enable running the project in an isolated container environment. It will define the Dockerfile and a guide for users, including considerations for API keys.

## Context
- `docs/SPEC.md`
- `docs/TASK_FORMAT.md`
- `docs/PLAN_SPECIFICATION.md`
- `docs/FEATURE_FORMAT.md`
- `docs/FILE_ORGANISATION.md`
- `docs/LOCAL_SETUP.md`
- `docs/AGENT_PRINCIPLES.md`
- `docs/TOOL_ARCHITECTURE.md`
- `docs/TESTING.md`
- `tasks/TASKS.md`
- `scripts/run_local_agent.py`
- `.env.example` (Implicit, for API keys)

## Features

11.1) - Create Docker directory and README
   Action: Create the `docs/docker` directory and the `RUNNING_DOCKER_README.md` file within it, detailing how to run the project in Docker.
   Acceptance:
   - `docs/docker/` directory exists.
   - `docs/docker/RUNNING_DOCKER_README.md` exists and contains initial instructions for setting up and running the project within Docker, including notes on environment variables and API keys.
   Context: `docs/FILE_ORGANISATION.md`, `docs/LOCAL_SETUP.md`
   Output: `docs/docker/RUNNING_DOCKER_README.md`

11.2) - Create Dockerfile
   Action: Create a basic `Dockerfile` that can build an image capable of running the agent.
   Acceptance:
   - `docs/docker/Dockerfile` exists.
   - The Dockerfile includes necessary instructions to set up Python, install dependencies from `requirements.txt`, and set up the working directory.
   Context: `requirements.txt` (implicitly needed for Dockerfile), `docs/LOCAL_SETUP.md`
   Output: `docs/docker/Dockerfile`

11.3) - Test Docker file and README creation
   Action: Create a simple test script to verify the existence of the created Docker files and their basic content.
   Acceptance:
   - `tasks/11/tests/test_docker_setup.py` exists.
   - The script verifies the existence of `docs/docker/RUNNING_DOCKER_README.md` and `docs/docker/Dockerfile`.
   Context: `docs/TESTING.md`, `docs/FILE_ORGANISATION.md`
   Output: `tasks/11/tests/test_docker_setup.py`

## Execution Steps
1) Create `tasks/11/plan_11.md` with the above plan.
2) Create the `docs/docker` directory (implicitly handled by `write_file` if the path includes directories).
3) Write the content for `docs/docker/RUNNING_DOCKER_README.md`.
4) Write the content for `docs/docker/Dockerfile`.
5) Write the test script `tasks/11/tests/test_docker_setup.py`.
6) Update `tasks/TASKS.md` to mark Task 11 as `+` Completed.
7) Submit for review.
8) Finish.
