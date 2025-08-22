import unittest
import os

class TestSpeccerSpec(unittest.TestCase):

    def setUp(self):
        self.spec_file = 'docs/AGENT_SPECCER.md'
        if not os.path.exists(self.spec_file):
            self.fail(f"{self.spec_file} does not exist.")
        with open(self.spec_file, 'r') as f:
            self.content = f.read()

    def test_1_file_exists(self):
        """The specification file `docs/AGENT_SPECCER.md` is created or updated."""
        self.assertTrue(os.path.exists(self.spec_file))

    def test_2_workflow_section(self):
        """The document outlines a clear workflow for the Speccer agent: 1. Analyze the task, 2. Create atomic features, 3. Finish the specification."""
        self.assertIn("## Workflow", self.content, "Workflow section is missing.")
        self.assertIn("Analyze", self.content, "Workflow step 'Analyze' is missing.")
        self.assertIn("Create", self.content, "Workflow step 'Create' is missing.")
        self.assertIn("Finish", self.content, "Workflow step 'Finish' is missing.")

    def test_3_tools_reference_section(self):
        """The document contains a 'Tools Reference' section detailing the agent's tools."""
        self.assertIn("## Tools Reference", self.content, "'Tools Reference' section is missing.")

    def test_4_create_feature_tool(self):
        """The 'Tools Reference' section defines the `create_feature(title: str, description: str)` tool and its purpose."""
        self.assertIn("create_feature(title: str, description: str)", self.content, "`create_feature` tool definition is missing or incorrect.")

    def test_5_finish_spec_tool(self):
        """The 'Tools Reference' section defines the `finish_spec()` tool and mandates its use upon completion."""
        self.assertIn("finish_spec()", self.content, "`finish_spec` tool definition is missing.")
        self.assertIn("**MUST** call the `finish_spec` tool to complete your assignment", self.content, "Mandate for using `finish_spec` is missing.")

    def test_6_block_task_tool(self):
        """The 'Tools Reference' section defines the `block_task(reason: str)` tool and mandates its use when blocked."""
        self.assertIn("block_task(reason: str)", self.content, "`block_task` tool definition is missing or incorrect.")
        self.assertIn("**MUST** use `block_task` to explain the reason for being stuck", self.content, "Mandate for using `block_task` is missing.")

    def test_7_file_organisation_reference(self):
        """The document explicitly references `docs/FILE_ORGANISATION.md` for context on project structure."""
        self.assertIn("docs/FILE_ORGANISATION.md", self.content, "Reference to `docs/FILE_ORGANISATION.md` is missing.")


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
