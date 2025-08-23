import os
import stat
import re

path = 'scripts/docker/run.sh'

# Criterion 1: File exists
assert os.path.exists(path), f"File {path} does not exist"

# Criterion 2: Executable permissions (mode at least 0o755)
mode = os.stat(path).st_mode
assert (mode & 0o777) >= 0o755, f"File {path} does not have sufficient permissions: {oct(mode & 0o777)}"

with open(path, 'r') as f:
    content = f.read()

# Criterion 3: Checks if image built and builds if not
assert re.search(r'docker\s+images\s+-q|docker\s+image\s+inspect', content), "No image check logic found"
assert re.search(r'docker-compose\s+build|docker\s+build', content), "No build command found"

# Criterion 4: Uses docker-compose up
assert 'docker-compose up' in content, "No 'docker-compose up' found"

# Criterion 5: Accepts and passes arguments (e.g., $@)
assert '$@' in content or ' "$@"' in content, "No argument passing (e.g., $@) found"

# Criterion 6: Handles graceful shutdown (trap SIGINT/SIGTERM and docker-compose down)
assert re.search(r'trap.*docker-compose\s+down.*SIGINT\s+SIGTERM', content), "No trap for shutdown found"

# Criterion 7: Reuses .env (source or mount)
assert re.search(r'source\s+.*\.env|-v\s+.*\.env', content), "No .env reuse found"

# Criterion 8: Launches with single command - inferred from existence and executability
# If all above pass, this should be true

print("All criteria passed!")