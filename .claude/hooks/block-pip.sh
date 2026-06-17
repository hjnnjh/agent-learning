#!/usr/bin/env bash
# PreToolUse(Bash) hook: reject pip/conda installs; enforce `uv`.
# Reads the tool input JSON from stdin, inspects the command string.
set -euo pipefail

input="$(cat)"
cmd="$(printf '%s' "$input" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("tool_input",{}).get("command",""))' 2>/dev/null || true)"

# Allow `uv pip ...`; block bare pip / pip3 / python -m pip / conda install.
if printf '%s' "$cmd" | grep -Eq '(^|[;&|[:space:]])(pip3?|python3?[[:space:]]+-m[[:space:]]+pip)[[:space:]]+install' \
   && ! printf '%s' "$cmd" | grep -Eq '(^|[;&|[:space:]])uv[[:space:]]+pip[[:space:]]+install'; then
  echo "REJECTED: 本项目强制用 uv 安装 Python 依赖。请改用 'uv add <pkg>' 或 'uv pip install <pkg>'。" >&2
  exit 2
fi
if printf '%s' "$cmd" | grep -Eq '(^|[;&|[:space:]])conda[[:space:]]+install'; then
  echo "REJECTED: 禁止 conda install。请改用 uv。" >&2
  exit 2
fi
exit 0
