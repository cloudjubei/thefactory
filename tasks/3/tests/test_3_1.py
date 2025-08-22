import unittest
from pathlib import Path

class TestGitignoreProjectsSubmodules(unittest.TestCase):
    def setUp(self):
        self.repo_root = Path('.')
        self.gitignore_path = self.repo_root / '.gitignore'

    def _read_gitignore_patterns(self):
        self.assertTrue(self.gitignore_path.exists(), ".gitignore must exist at the repository root")
        lines = self.gitignore_path.read_text(encoding='utf-8').splitlines()
        patterns = []
        for raw in lines:
            s = raw.strip()
            if not s:
                continue
            if s.startswith('#'):
                continue
            patterns.append(s)
        return patterns

    def test_projects_directory_is_ignored_and_gitmodules_not_ignored(self):
        patterns = self._read_gitignore_patterns()

        # Acceptance: projects/ directory and all contents are ignored
        projects_ignore_ok = any(
            p in ('projects/', '/projects/', 'projects/**', '/projects/**')
            for p in patterns
        )
        self.assertTrue(
            projects_ignore_ok,
            "Expected .gitignore to include a rule that ignores the entire 'projects/' directory (e.g., 'projects/' or '/projects/' or 'projects/**')."
        )

        # Acceptance: .gitmodules is explicitly unignored
        has_unignore_gitmodules = any(
            p in ('!.gitmodules', '!/.gitmodules') for p in patterns
        )
        self.assertTrue(
            has_unignore_gitmodules,
            "Expected .gitignore to explicitly unignore .gitmodules (e.g., '!.gitmodules')."
        )

        # Acceptance: .gitmodules is not directly ignored
        ignores_gitmodules_directly = any(
            p in ('.gitmodules', '/.gitmodules') for p in patterns
        )
        self.assertFalse(
            ignores_gitmodules_directly,
            "Found a rule that directly ignores .gitmodules, which would break submodule tracking."
        )

if __name__ == '__main__':
    unittest.main()