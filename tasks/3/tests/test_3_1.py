import os
import re
import unittest

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(ROOT, '..'))

GUIDE_PATH = os.path.join(REPO_ROOT, 'docs', 'PROJECTS_GUIDE.md')
FILE_ORG_PATH = os.path.join(REPO_ROOT, 'docs', 'FILE_ORGANISATION.md')

class TestProjectsGuide(unittest.TestCase):
    def read_file(self, path):
        self.assertTrue(os.path.exists(path), f"Missing required file: {path}")
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    def test_guide_exists(self):
        _ = self.read_file(GUIDE_PATH)

    def test_file_organisation_mentions_guide(self):
        content = self.read_file(FILE_ORG_PATH)
        self.assertRegex(content, r'PROJECTS_GUIDE\.md', "docs/FILE_ORGANISATION.md must reference PROJECTS_GUIDE.md")

    def test_overview_and_projects_folder(self):
        content = self.read_file(GUIDE_PATH)
        self.assertRegex(content, r'(?i)overview', "Guide should include an Overview section")
        self.assertIn('projects/', content, "Guide should reference the projects/ folder")
        self.assertRegex(content, r'(?is)projects/.+submodule', "Overview should state projects are git submodules")

    def test_required_commands_present(self):
        content = self.read_file(GUIDE_PATH)
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
            self.assertIn(cmd, content, f"Guide must include command: {cmd}")
        # Ensure path examples use projects/<name>
        self.assertIn('projects/<name>', content, "Guide must illustrate submodules using projects/<name> path")

    def test_clone_and_init_instructions(self):
        content = self.read_file(GUIDE_PATH)
        self.assertIn('git clone --recurse-submodules', content, "Must document clone with recurse-submodules")
        self.assertIn('git submodule init', content, "Must document submodule init")
        self.assertIn('git submodule update --init --recursive', content, "Must document combined init/update")

    def test_add_submodule_and_commits(self):
        content = self.read_file(GUIDE_PATH)
        self.assertRegex(content, r'git\s+submodule\s+add\s+-b\s+<branch>\s+<url>\s+projects/<name>', "Must show git submodule add -b <branch> <url> projects/<name>")
        # Mention committing .gitmodules and pointer update
        self.assertRegex(content, r'(?is)commit.*\.gitmodules', "Must mention committing .gitmodules when adding")
        self.assertRegex(content, r'(?is)commit.*pointer|pointer.*commit', "Must mention committing the submodule pointer update")

    def test_update_methods_and_foreach(self):
        content = self.read_file(GUIDE_PATH)
        self.assertIn('git submodule update --remote', content, "Must include update --remote")
        self.assertRegex(content, r'(?is)enter(ing)?\s+the\s+submodule.+pull', "Must describe entering submodule and pulling")
        self.assertRegex(content, r'(?is)commit.+pointer|pointer.+commit', "Must mention committing pointer bump in superproject")
        self.assertIn('git submodule foreach', content, "Must provide foreach example for bulk ops")

    def test_switch_tracked_branch(self):
        content = self.read_file(GUIDE_PATH)
        self.assertRegex(content, r'git\s+config\s+-f\s+\.gitmodules\s+submodule\.projects/<name>\.branch\s+<branch>', "Must document switching tracked branch via .gitmodules config")
        self.assertRegex(content, r'(?is)commit.*\.gitmodules', "Must mention committing .gitmodules when switching branch")

    def test_remove_submodule(self):
        content = self.read_file(GUIDE_PATH)
        self.assertIn('git submodule deinit -f projects/<name>', content, "Must include deinit command")
        self.assertIn('git rm -f projects/<name>', content, "Must include git rm command")
        self.assertIn('rm -rf .git/modules/projects/<name>', content, "Must include removing .git/modules path")
        self.assertRegex(content, r'(?is)\.gitmodules.+(updated|edit)', "Must note .gitmodules is updated")
        self.assertRegex(content, r'(?is)commit.+\.gitmodules', "Must note committing .gitmodules changes")

    def test_common_pitfalls(self):
        content = self.read_file(GUIDE_PATH)
        self.assertRegex(content, r'(?i)common\s+pitfalls', "Must include a Common pitfalls section")
        pitfalls_checks = [
            ('detached HEAD', r'(?i)detached\s+HEAD'),
            ('uncommitted changes', r'(?i)uncommitted\s+changes'),
            ('mixing SSH and HTTPS', r'(?is)(SSH).+(HTTPS)|(HTTPS).+(SSH)'),
            ('forgetting to commit .gitmodules', r'(?is)commit.+\.gitmodules'),
            ('not committing the submodule pointer update', r'(?is)not.+commit.+pointer|pointer.+not.+commit'),
            ('needing git submodule sync when URLs change', r'(?is)submodule\s+sync.+URL'),
            ('ensuring CI uses --init --recursive', r'(?is)CI.+--init\s+--recursive'),
        ]
        for name, pattern in pitfalls_checks:
            self.assertRegex(content, pattern, f"Pitfall missing or unclear: {name}")

    def test_cicd_notes(self):
        content = self.read_file(GUIDE_PATH)
        self.assertRegex(content, r'(?i)CI/?CD', "Must have CI/CD notes section")
        self.assertIn('git clone --recurse-submodules', content, "CI/CD must show clone with recurse-submodules")
        self.assertIn('git submodule update --init --recursive', content, "CI/CD must show submodule update --init --recursive")

    def test_troubleshooting(self):
        content = self.read_file(GUIDE_PATH)
        self.assertRegex(content, r'(?i)troubleshooting', "Must include Troubleshooting section")
        self.assertIn('git submodule sync', content, "Troubleshooting must include git submodule sync")
        self.assertIn('git submodule status', content, "Troubleshooting must include git submodule status")

    def test_quick_reference(self):
        content = self.read_file(GUIDE_PATH)
        self.assertRegex(content, r'(?i)(quick\s*reference|cheat\s*sheet)', "Must include a Quick reference or cheat sheet section")

    def test_commit_flow_guidance(self):
        content = self.read_file(GUIDE_PATH)
        # Ensure it states changes inside a submodule are committed in the submodule, then superproject pointer updated/committed
        self.assertRegex(content, r'(?is)changes?.+inside\s+a\s+submodule.+commit(ed|)\s+within', "Must say to commit changes within the submodule")
        self.assertRegex(content, r'(?is)superproject.+pointer.+commit', "Must say to update and commit the pointer in the superproject")

    def test_authentication_schemes(self):
        content = self.read_file(GUIDE_PATH)
        self.assertRegex(content, r'(?is)SSH', "Must discuss SSH")
        self.assertRegex(content, r'(?is)HTTPS', "Must discuss HTTPS")
        self.assertRegex(content, r'(?is)mix|avoid\s+mix(ing)?', "Must warn about mixing auth schemes")
        self.assertRegex(content, r'(?is)CI', "Must mention CI context for auth consideration")

if __name__ == '__main__':
    unittest.main()
