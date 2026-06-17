#!/usr/bin/env bash
# PostToolUse(Write|Edit) hook: run ruff format + check on edited .py files.
# No-op if the edited file is not Python or if ruff is unavailable.
set -euo pipefail

input="$(cat)"
path="$(printf '%s' "$input" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("tool_input",{}).get("file_path",""))' 2>/dev/null || true)"

case "$path" in
  *.py) ;;
  *) exit 0 ;;
esac
[ -f "$path" ] || exit 0

if command -v ruff >/dev/null 2>&1; then
  ruff format "$path" >/dev/null 2>&1 || true
  ruff check --fix "$path" || true
elif command -v uv >/dev/null 2>&1; then
  uv run ruff format "$path" >/dev/null 2>&1 || true
  uv run ruff check --fix "$path" || true
else
  echo "提示：未检测到 ruff（uv add --dev ruff 可启用自动检查）。" >&2
fi
exit 0
