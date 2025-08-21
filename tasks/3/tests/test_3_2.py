import os, sys

def run():
    proj_dir = "projects"
    if not os.path.isdir(proj_dir):
        print(f"FAIL: '{proj_dir}/' directory does not exist.")
        sys.exit(1)

    gi_path = ".gitignore"
    if not os.path.exists(gi_path):
        print("FAIL: .gitignore does not exist at repository root.")
        sys.exit(1)

    with open(gi_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]

    if "/projects/" not in lines:
        print("FAIL: .gitignore does not contain the required '/projects/' line.")
        sys.exit(1)

    print("PASS: projects/ directory exists and .gitignore contains '/projects/'.")
    sys.exit(0)

if __name__ == "__main__":
    run()
