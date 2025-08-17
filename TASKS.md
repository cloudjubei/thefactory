# Tasks

See **[TASK_FORMAT.md](TASK_FORMAT.md)** for format reference and how to write acceptance criteria.

## Current Tasks

0) + Initial spec document
   Action: Create the founding SPEC.md document
   Acceptance: SPEC.md exists with WHAT, CORE IDEAS and ACTIONS sections

1) = Specification documentation
   Action: Analyse the specification format and what requirements it needs to provide.
   Acceptance: SPECIFICATION_GUIDE.md exists describing format, SPEC.md adheres to this format

2) + First tasks
   Description: Create the initial task list for the project
   Acceptance: TASKS.md exists with at least 3 tasks and at least 1 pending task

3) = Task format
   Action: Analyse the tasks and what requirements they need to provide. All the format and specification for that should be included in the documentation.
   Acceptance: TASK_FORMAT.md exists describing the format, TASKS.md adheres to this format

4) = Specification template
   Action: Create a reusable template for writing new specifications
   Acceptance: TEMPLATE.md exists with all required sections from SPECIFICATION_GUIDE.md, with examples for each
   Dependencies: 1

5) - Allow Autonomous Agents to produce changes
   Action: Create a workflow so that an AI agent can create a change to the project (relating to a task) by committing them and creating a Pull Request for it to be reviewed.
   Acceptance: A commit with some changes is made and a Pull Request is opened for it.
   Dependencies: 2,6

6) + Specify the Autonomous Agent Workflow
   Action: Define the step-by-step process an autonomous agent will follow to select a task, make changes to the repository, and create a pull request. This specification should also define the tools and permissions the agent will require.
   Acceptance: AGENT_WORKFLOW.md exists, detailing the agent's decision-making process, how it interacts with the git repository, and the format of its pull requests.

7) + Implement a Basic Git Interaction Script for the Agent
    Action: Create a script that can perform the basic git operations required for the autonomous agent. This includes cloning the repository, creating a new branch, committing changes, and pushing the branch to the remote repository.
    Acceptance: A script (e.g., in Python or Bash) is created in a new scripts/ directory. The script can be manually triggered to perform the specified git operations.
    Dependencies: 6

8) - Set up a GitHub Action to Automate the Agent's Workflow
    Action: Create a GitHub Actions workflow that automates the execution of the agent's tasks. This workflow should be triggerable on a specific event (e.g., a new issue being labeled for the agent).
    Acceptance: A new workflow file, agent_workflow.yml, is added to the .github/workflows/ directory. This workflow successfully runs the git interaction script and creates a pull request.
    Dependencies: 7
    
9) - Test Agent Automation
   Action: This is a test task for the GitHub Actions workflow to pick up.
   Acceptance: The agent creates a file named `task_9_output.md` and opens a PR.