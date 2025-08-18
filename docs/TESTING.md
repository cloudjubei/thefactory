# Testing Specification

## 1. Philosophy

The primary goal of testing is to verify that the agent can correctly interpret tasks and generate valid, effective sequences of tool calls to satisfy the task's acceptance criteria. Our testing philosophy is guided by these principles:

-   **Behavior-Driven:** We test the agent's observable output (its JSON plan and tool calls), not its internal reasoning process. This treats the LLM as a black box.
-   **Deterministic & Repeatable:** Tests must produce the same result every time. This is achieved by mocking the LLM's response and providing a controlled file system environment for each test.
-   **Comprehensive:** Tests should cover a wide range of scenarios, from simple file creation to complex, multi-step tasks and error conditions.

## 2. Types of Tests

### 2.1. Unit Tests
-   **Purpose:** To test individual tools in isolation.
-   **Location:** `tests/unit/`
-   **Implementation:** Standard Python unit tests (e.g., using `pytest`) that call the tool functions directly and assert their return values and side effects (like file creation).

### 2.2. End-to-End (E2E) Tests
-   **Purpose:** To test the agent's ability to complete a full task cycle. This is the most important type of test for verifying agent capabilities.
-   **Location:** `tests/e2e/`
-   **Implementation:** A test harness script (`scripts/run_tests.py`) will orchestrate E2E tests. Each test simulates a full run of the `run_local_agent.py` script against a specific task, using a mocked LLM response.

## 3. Test Harness

The test harness is a script responsible for:
1.  Reading a test case definition file (in YAML).
2.  Setting up a temporary, isolated environment (e.g., a temporary directory).
3.  Populating the environment with any required mock files (e.g., a simplified `TASKS.md`).
4.  Executing the agent's tool calls (using a mocked agent response defined in the test case).
5.  Running assertions against the final state of the environment (e.g., checking file contents, verifying PR creation calls).
6.  Cleaning up the environment.

## 4. Test Case Structure

E2E tests are defined in YAML files for clarity and readability. Each file, named `tests/e2e/test_{task_id}.yaml`, will follow this structure:

```yaml
test_name: "A descriptive name for the test case"
task_id: The integer ID of the task being tested

# Describes the initial state of the file system
setup:
  mock_files:
    - path: "tasks/TASKS.md"
      content: |
        8) - Test Task
           Action: Do something.
           Acceptance: The file 'output.txt' is created.

# The exact JSON response the agent is expected to produce.
# This avoids actual LLM calls, making the test fast and deterministic.
mock_agent_response:
  plan: "My plan is to create the file and complete the task."
  tool_calls:
    - tool_name: "write_file"
      arguments:
        path: "output.txt"
        content: "Success"
    - tool_name: "write_file"
      arguments:
        path: "tasks/TASKS.md"
        content: |
          8) + Test Task
             Action: Do something.
             Acceptance: The file 'output.txt' is created.
    - tool_name: "submit_for_review"
      arguments:
        task_id: 8
        task_title: "Test Task"
    - tool_name: "finish"
      arguments:
        reason: "Task completed successfully."

# Conditions to verify after the tool calls have been executed
assertions:
  # Verifies a file exists at the given path
  - type: "file_exists"
    path: "output.txt"

  # Verifies the content of a file exactly matches the expected content
  - type: "file_matches"
    path: "output.txt"
    content: "Success"

  # Verifies the file contains a specific substring
  - type: "file_contains"
    path: "tasks/TASKS.md"
    content: "8) + Test Task"

  # Verifies that the 'submit_for_review' tool was called with the correct details
  - type: "pr_created"
    task_id: 8
    title_contains: "Test Task"
```

## 5. Workflow for Adding a New Test

1.  **Create the Test File:** For a new Task `N`, create `tests/e2e/test_N.yaml`.
2.  **Define the Initial State:** In the `setup` section, specify the files the agent needs to read (e.g., `TASKS.md`, relevant spec files).
3.  **Define the Expected Behavior:** Craft the ideal `mock_agent_response` JSON that a perfect agent would generate to solve the task.
4.  **Define Success:** In the `assertions` section, list the conditions that prove the task was completed successfully (e.g., files were created/modified correctly, the PR was created).
5.  **Run the Test:** Execute the test harness: `python3 scripts/run_tests.py --task N`.