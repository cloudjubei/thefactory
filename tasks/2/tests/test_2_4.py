import os

def test_requirements():
    assert os.path.exists('requirements.txt'), "requirements.txt does not exist"
    with open('requirements.txt', 'r') as f:
        content = f.read()
    assert 'litellm' in content, "litellm not in requirements.txt"
    assert 'python-dotenv' in content, "python-dotenv not in requirements.txt"

if __name__ == "__main__":
    try:
        test_requirements()
        print("All tests passed.")
    except AssertionError as e:
        print(f"Test failed: {e}")
        raise