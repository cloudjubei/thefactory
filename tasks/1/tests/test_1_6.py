import sys
import os

def run():
    file_path = "docs/TESTING.md"
    if not os.path.exists(file_path):
        print(f"FAIL: {file_path} does not exist.")
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Acceptance Criterion: Check for key sections/topics
    required_topics = [
        "Purpose and Scope",
        "Test Locations and Naming Conventions",
        "Test Structure and Utilities",
        "Writing Acceptance Tests",
        "Running Tests",
        "Tool Usage",
        "finish_feature"
    ]

    missing = [topic for topic in required_topics if topic not in content]

    if missing:
        print(f"FAIL: Missing topics in {file_path}: {', '.join(missing)}")
        sys.exit(1)

    print(f"PASS: {file_path} exists and describes the testing specification as required.")
    sys.exit(0)

if __name__ == "__main__":
    run()
