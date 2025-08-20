import unittest
import tempfile
import shutil
import os
import json
import sys

# Add script directory to path to allow import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../scripts')))
from migrate_tasks import parse_plan_md, migrate_task

class TestPlanMigration(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.tasks_dir = os.path.join(self.test_dir, 'tasks')
        os.makedirs(self.tasks_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_parse_plan_md(self):
        content = """
This is the main task plan.
It can span multiple lines.

### 1.1 First Feature
This is the plan for the first feature.

### 1.2 Second Feature
And this is the plan for the second.
It also has multiple lines.
"""
        main_plan, feature_plans = parse_plan_md(content)
        self.assertEqual(main_plan, "This is the main task plan.\nIt can span multiple lines.")
        self.assertIn("1.1", feature_plans)
        self.assertEqual(feature_plans["1.1"], "This is the plan for the first feature.")
        self.assertIn("1.2", feature_plans)
        self.assertEqual(feature_plans["1.2"], "And this is the plan for the second.\nIt also has multiple lines.")

    def test_migrate_task(self):
        # Create dummy task structure
        task_1_path = os.path.join(self.tasks_dir, '1')
        os.makedirs(task_1_path)

        task_json_content = {
            "id": 1,
            "title": "Test Task",
            "plan": "Initial plan.",
            "features": [
                {"id": "1.1", "title": "Feature 1"},
                {"id": "1.2", "title": "Feature 2", "plan": "Initial feature plan."}
            ]
        }
        with open(os.path.join(task_1_path, 'task.json'), 'w') as f:
            json.dump(task_json_content, f)

        plan_md_content = """
Main plan from markdown.

### 1.1 First One
Plan for feature 1.1.

### 1.2 Second One
Plan for feature 1.2.
"""
        with open(os.path.join(task_1_path, 'plan.md'), 'w') as f:
            f.write(plan_md_content)

        # Run migration
        result = migrate_task(task_1_path)
        self.assertTrue(result)

        # Verify results
        self.assertFalse(os.path.exists(os.path.join(task_1_path, 'plan.md')))

        with open(os.path.join(task_1_path, 'task.json'), 'r') as f:
            updated_task_data = json.load(f)
        
        self.assertEqual(updated_task_data['plan'], "Initial plan.\nMain plan from markdown.")
        
        feature1 = updated_task_data['features'][0]
        self.assertEqual(feature1['id'], '1.1')
        self.assertEqual(feature1['plan'], "Plan for feature 1.1.")
        
        feature2 = updated_task_data['features'][1]
        self.assertEqual(feature2['id'], '1.2')
        self.assertEqual(feature2['plan'], "Initial feature plan.\nPlan for feature 1.2.")

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPlanMigration))
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    if result.wasSuccessful():
        print("PASS: All tests passed.")
        sys.exit(0)
    else:
        print("FAIL: Some tests failed.")
        sys.exit(1)
