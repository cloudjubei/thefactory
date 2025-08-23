import unittest
import os
import re

class TestSubmoduleDocumentation(unittest.TestCase):
    """
    Tests for the submodule documentation feature (3.1).
    This test suite verifies that the documentation file docs/PROJECTS_GUIDE.md
    is comprehensive and meets all the acceptance criteria.
    """
    projects_guide_path = 'docs/PROJECTS_GUIDE.md'
    file_org_path = 'docs/FILE_ORGANISATION.md'
    projects_guide_content = ""
    file_org_content = ""

    @classmethod
    def setUpClass(cls):
        """Load file contents once for all tests."""
        if not os.path.exists(cls.projects_guide_path):
            raise FileNotFoundError(f"{cls.projects_guide_path} not found.")
        with open(cls.projects_guide_path, 'r', encoding='utf-8') as f:
            cls.projects_guide_content = f.read()

        if not os.path.exists(cls.file_org_path):
            raise FileNotFoundError(f"{cls.file_org_path} not found.")
        with open(cls.file_org_path, 'r', encoding='utf-8') as f:
            cls.file_org_content = f.read()

    def test_file_existence_and_reference(self):
        """
        Criteria 1 & 2: Check that docs/PROJECTS_GUIDE.md exists and is
        referenced in docs/FILE_ORGANISATION.md.
        """
        self.assertTrue(os.path.exists(self.projects_guide_path))
        self.assertIn('docs/PROJECTS_GUIDE.md', self.file_org_content,
                      "FILE_ORGANISATION.md should reference PROJECTS_GUIDE.md")

    def test_core_content_sections(self):
        """
        Criteria 3, 9, 10, 11, 12, 15: Check for presence of all required sections
        and key content within them.
        """
        content = self.projects_guide_content
        # C3: Overview
        self.assertIn('## Overview', content)
        self.assertIn('projects/ directory contains child projects, each tracked as a Git submodule', content)

        # C15: Authentication
        self.assertIn('## Authentication: SSH vs HTTPS', content)
        self.assertIn('Mixing SSH and HTTPS', content)

        # C10: CI/CD
        self.assertIn('## CI/CD notes', content)

        # C11: Troubleshooting
        self.assertIn('## Troubleshooting', content)
        
        # C9: Common pitfalls
        self.assertIn('## Common pitfalls', content)
        pitfalls_section = re.search(r'## Common pitfalls\n(.*?)\n##', content, re.DOTALL | re.IGNORECASE)
        self.assertIsNotNone(pitfalls_section, "Common pitfalls section not found.")
        pitfalls_text = pitfalls_section.group(1)
        self.assertIn('Detached HEAD', pitfalls_text)
        self.assertIn('Uncommitted changes', pitfalls_text)
        self.assertIn('Forgetting to commit .gitmodules', pitfalls_text)
        self.assertIn('Not committing the submodule pointer update', pitfalls_text)

        # C12: Quick reference / cheat sheet
        self.assertIn('## Quick reference / cheat sheet', content)

    def test_workflow_instructions(self):
        """
        Criteria 4, 5, 6, 7, 8: Verify that instructions for the main submodule
        workflows (clone, add, update, switch branch, remove) are present.
        """
        content = self.projects_guide_content
        # C4: Cloning
        self.assertIn('git clone --recurse-submodules', content)
        self.assertIn('git submodule update --init --recursive', content)

        # C5: Adding
        self.assertIn('git submodule add -b', content)
        self.assertIn('you must commit both', content, "Missing instruction to commit .gitmodules and submodule pointer after add")
        self.assertIn('git add .gitmodules projects/<name>', content)

        # C6: Updating
        self.assertIn('git submodule update --remote', content)
        self.assertIn('git submodule foreach', content)
        self.assertIn('commit the new pointer in the superproject', content)

        # C7: Switching branch
        self.assertIn('git config -f .gitmodules submodule.projects/<name>.branch', content)
        self.assertIn('commit -m "Track <branch> for projects/<name>"', content, "Missing instruction to commit .gitmodules after branch switch")

        # C8: Removing
        self.assertIn('git submodule deinit -f', content)
        self.assertIn('git rm -f projects/<name>', content)
        self.assertIn('rm -rf .git/modules/projects/<name>', content)

    def test_path_conventions_and_pointer_commits(self):
        """
        Criterion 13: Check for consistent use of `projects/<name>` path and
        clear instructions about committing submodule pointer changes.
        """
        content = self.projects_guide_content
        self.assertGreaterEqual(content.count('projects/<name>'), 10, "Path 'projects/<name>' should be used consistently in examples.")
        self.assertIn('commit the updated submodule pointer', content)

    def test_all_required_commands_are_documented(self):
        """
        Criterion 14: Exhaustively verify that all specified git commands
        are mentioned in the documentation.
        """
        content = self.projects_guide_content
        commands = [
            'git clone --recurse-submodules',
            'git submodule init',
            'git submodule update',
            'git submodule update --init --recursive',
            'git submodule add -b',
            'git submodule update --remote',
            'git submodule foreach',
            'git submodule status',
            'git config -f .gitmodules submodule.projects/<name>.branch',
            'git submodule deinit -f',
            'git rm -f projects/<name>',
            'rm -rf .git/modules/projects/<name>',
            'git submodule sync',
        ]
        for cmd in commands:
            self.assertIn(cmd, content, f"Command '{cmd}' not found in PROJECTS_GUIDE.md")

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
