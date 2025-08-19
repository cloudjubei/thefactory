import os, sys, json, importlib.util, dataclasses, enum, glob

REQUIRED_DATACLASSES = [
    "Task", "Feature", "Context", "Output", "AcceptanceCriteria", "Rejection"
]
REQUIRED_ENUMS = [
    "TaskStatus", "FeatureStatus"
]

MODULE_PATH = os.path.join("docs", "tasks", "task_format.py")
EXAMPLE_JSON_PATH = os.path.join("docs", "tasks", "task_example.json")
NEW_GUIDE_PATH = os.path.join("docs", "tasks", "TASKS_GUIDANCE.md")
OLD_GUIDE_PATH = os.path.join("docs", "TASK_FORMAT.md")


def load_module_from_path(path, module_name="task_format"):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        return None
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)  # type: ignore[attr-defined]
        return mod
    except Exception:
        return None


def assert_true(condition, message):
    if not condition:
        print(f"FAIL: {message}")
        sys.exit(1)


def run():
    # 1) Check module existence
    if not os.path.exists(MODULE_PATH):
        print(f"FAIL: {MODULE_PATH} does not exist. Expected typed interfaces (dataclasses and Enums).")
        sys.exit(1)

    mod = load_module_from_path(MODULE_PATH)
    assert_true(mod is not None, f"Failed to import module from {MODULE_PATH}.")

    # 2) Check required dataclasses
    for name in REQUIRED_DATACLASSES:
        assert_true(hasattr(mod, name), f"Missing dataclass '{name}' in task_format.py")
        obj = getattr(mod, name)
        assert_true(dataclasses.is_dataclass(obj), f"'{name}' must be a @dataclass")

    # 3) Check required Enums and that values are strings
    for name in REQUIRED_ENUMS:
        assert_true(hasattr(mod, name), f"Missing Enum '{name}' in task_format.py")
        obj = getattr(mod, name)
        assert_true(isinstance(obj, type) and issubclass(obj, enum.Enum), f"'{name}' must be an Enum subclass")
        # Ensure all enum values are strings
        for member in obj:
            assert_true(isinstance(member.value, str), f"Enum '{name}' member '{member.name}' must serialize to a string value")

    # 4) Serialization functions for round-trip
    assert_true(hasattr(mod, "task_from_json"), "task_format.py must provide function task_from_json(json_str) -> Task")
    assert_true(hasattr(mod, "task_to_json"), "task_format.py must provide function task_to_json(task: Task) -> str")
    task_from_json = getattr(mod, "task_from_json")
    task_to_json = getattr(mod, "task_to_json")
    assert_true(callable(task_from_json), "task_from_json must be callable")
    assert_true(callable(task_to_json), "task_to_json must be callable")

    # 5) Example JSON exists
    if not os.path.exists(EXAMPLE_JSON_PATH):
        print(f"FAIL: {EXAMPLE_JSON_PATH} does not exist. Provide an example that validates against the interfaces.")
        sys.exit(1)

    with open(EXAMPLE_JSON_PATH, "r", encoding="utf-8") as f:
        example_json_str = f.read()
    # Validate it's valid JSON before passing to loader
    try:
        parsed = json.loads(example_json_str)
    except Exception as e:
        print(f"FAIL: {EXAMPLE_JSON_PATH} is not valid JSON: {e}")
        sys.exit(1)
    assert_true(isinstance(parsed, dict), "Example JSON must be an object at top-level")

    # Round-trip: json -> Task -> json -> Task and compare
    try:
        task_obj_1 = task_from_json(example_json_str)
    except Exception as e:
        print(f"FAIL: task_from_json raised an exception: {e}")
        sys.exit(1)

    try:
        json_str_2 = task_to_json(task_obj_1)
        parsed_2 = json.loads(json_str_2)
        task_obj_2 = task_from_json(json_str_2)
    except Exception as e:
        print(f"FAIL: Round-trip serialization failed: {e}")
        sys.exit(1)

    # Compare as dataclasses using asdict for structural equality; Enums -> their values
    def normalize(obj):
        def enum_to_value(x):
            if isinstance(x, enum.Enum):
                return x.value
            return x
        if dataclasses.is_dataclass(obj):
            d = dataclasses.asdict(obj)
            # Convert any Enums nested within to their values for stable comparison
            def convert(v):
                if isinstance(v, list):
                    return [convert(i) for i in v]
                if isinstance(v, dict):
                    return {k: convert(vv) for k, vv in v.items()}
                return enum_to_value(v)
            return convert(d)
        if isinstance(obj, dict):
            return {k: normalize(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [normalize(v) for v in obj]
        return enum_to_value(obj)

    norm1 = normalize(task_obj_1)
    norm2 = normalize(task_obj_2)
    assert_true(norm1 == norm2, "Round-trip Task object mismatch after serialization/deserialization")

    # 6) Guidance doc moved and references updated
    # New guidance exists
    assert_true(os.path.exists(NEW_GUIDE_PATH), f"{NEW_GUIDE_PATH} must exist (moved guidance doc)")
    # Old guidance removed
    assert_true(not os.path.exists(OLD_GUIDE_PATH), f"{OLD_GUIDE_PATH} should be removed after migration")

    # No references to old path across docs
    md_files = glob.glob(os.path.join("docs", "**", "*.md"), recursive=True)
    offenders = []
    for p in md_files:
        try:
            with open(p, "r", encoding="utf-8") as f:
                content = f.read()
            if "docs/TASK_FORMAT.md" in content:
                offenders.append(p)
        except Exception:
            # skip unreadable
            pass
    assert_true(len(offenders) == 0, "References to 'docs/TASK_FORMAT.md' remain in: " + ", ".join(offenders))

    # New guidance should mention JSON and task_format.py to indicate it's updated to new format
    with open(NEW_GUIDE_PATH, "r", encoding="utf-8") as f:
        new_guide = f.read()
    has_json = ("json" in new_guide.lower())
    mentions_module = ("task_format.py" in new_guide)
    assert_true(has_json and mentions_module, f"{NEW_GUIDE_PATH} should reference JSON format and task_format.py")

    print("PASS: Task 11.1 tests passed: interfaces, round-trip, and guidance doc checks.")
    sys.exit(0)


if __name__ == "__main__":
    run()
