# File Organisation

## Purpose
This document provides a scheme for organizing files within the repository, detailing the structure and naming conventions for different types of files.

## Structure and Naming Conventions

- **Specifications:**
  - All specification documents should be located in the root directory. They should follow the naming pattern `SPEC_<description>.md`.
  - Examples: `SPEC.md`, `SPECIFICATION_GUIDE.md`, `AGENT_PRINCIPLES.md`

- **Tasks:**
  - Tasks are maintained in `TASKS.md` located in the root directory.

- **Guides and Documentation:**
  - Files like guides and other documentation should be located in the root and named descriptively.
  - Examples: `SPECIFICATION_GUIDE.md`, `TASK_FORMAT.md`

- **Scripts:**
  - All scripts should be in a `scripts/` directory.
  - Naming should follow the lowercase and underscore-separated format. E.g., `scripts/run_local_agent.py`

- **Configuration and Dependencies:**
  - Configuration files like `.env.example` as well as dependency files like `requirements.txt` should be in the root directory.

- **Plans and Templates:**
  - Plans should be in the `plans/` directory with descriptive file names.
  - Templates are in the root directory or within relevant folders based on their use.

## Adhering to Organization
All existing files should follow the above structure and naming conventions as of the creation of this document.