import json
import os

def test_example_task_file():
    file_path = 'docs/tasks/task_example.json'
    assert os.path.exists(file_path), f"File {file_path} does not exist"
    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
            assert isinstance(data, dict), "Loaded JSON is not an object"
        except json.JSONDecodeError:
            assert False, "File does not contain a valid JSON object"
    # Basic conformance to Task schema
    required_fields = {
        'id': str,
        'name': str,
        'description': str,
        'acceptance': list
    }
    for field, field_type in required_fields.items():
        assert field in data, f"Missing required field: {field}"
        assert isinstance(data[field], field_type), f"Field {field} has incorrect type: expected {field_type.__name__}, got {type(data[field]).__name__}"
    for item in data['acceptance']:
        assert isinstance(item, str), "Acceptance criteria items must be strings"