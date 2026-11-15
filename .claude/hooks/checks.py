"""PostToolUse hook: run ruff and mypy after every file edit."""
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent.parent
venv_bin = root / ".venv" / "bin"

failed = False

for cmd in [
    [str(venv_bin / "ruff"), "check", "app", "tests"],
    [str(venv_bin / "mypy"), "app"],
]:
    result = subprocess.run(cmd, cwd=root, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stdout, file=sys.stderr, end="")
        print(result.stderr, file=sys.stderr, end="")
        failed = True

if failed:
    sys.exit(1)
