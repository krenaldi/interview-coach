"""PreToolUse hook: block Read calls that target .env files."""
import json
import sys

tool_input = json.load(sys.stdin)
path = tool_input.get("file_path", "")

if ".env" in path and ".env.example" not in path:
    print(f"Blocked: reading {path} is not allowed — use .env.example as a reference.", file=sys.stderr)
    sys.exit(2)
