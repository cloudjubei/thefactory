import unittest
from pathlib import Path

class TestChildProjectsSubmodulesDocs(unittest.TestCase):
    DOC_PATH = Path("docs/projects-submodules.md")

    @classmethod
    def setUpClass(cls):
        cls.text = ""
        if cls.DOC_PATH.exists():
            cls.text = cls.DOC_PATH.read_text(encoding="utf-8")
        cls.lower = cls.text.lower()

    def test_doc_exists(self):
        self.assertTrue(self.DOC_PATH.exists(), f"Expected documentation at {self.DOC_PATH}. Create the doc describing submodule workflow under projects/.")

    def test_sections_present(self):
        # Required conceptual sections by heading or phrase presence
        required_sections = [
            "overview",
            "clone with submodules",
            "initialize existing clone",
            "add a child project",
            "update submodules",
            "switch submodule branch",
            "remove a child project",
            "common pitfalls",
            "ci/cd",
            "troubleshooting",
            "quick reference",
        ]
        missing = [s for s in required_sections if s not in self.lower]
        self.assertFalse(missing, f"Missing required sections/headings: {missing}")

    def test_required_commands_and_content(self):
        # Presence of key commands and concepts
        required_phrases = [
            # Paths and files
            "projects/",
            "projects/<name>",
            ".gitmodules",
            ".git/modules/projects/",
            # Clone/init
            "git clone --recurse-submodules",
            "git submodule init",
            "git submodule update",
            "git submodule update --init --recursive",
            # Add
            "git submodule add -b",
            # Update
            "git submodule update --remote",
            "git submodule foreach",
            "git submodule status",
            # Switch branch
            "git config -f .gitmodules submodule.projects/",
            # Remove
            "git submodule deinit -f",
            "git rm -f projects/",
            # Sync and troubleshooting
            "git submodule sync",
            # Pitfalls and guidance
            "detached head",
            "commit .gitmodules",
            "submodule pointer",
            # Auth and CI/CD
            "ssh",
            "https",
            "ci",
        ]
        missing = [p for p in required_phrases if p.lower() not in self.lower]
        self.assertFalse(missing, "Missing required phrases/commands in the documentation: " + ", ".join(missing))

if __name__ == "__main__":
    unittest.main()