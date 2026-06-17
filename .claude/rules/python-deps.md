---
type: "auto"
---

# Python Dependency Installation Rule

**MUST** use `uv` to install every Python dependency.

- **MUST**: `uv add <package>` (project deps) or `uv pip install <package>`
- **MUST NOT**: `pip install`, `pip3 install`, `python -m pip install`
- **MUST NOT**: `conda install`
- **MUST NOT**: auto-install dependencies with any tool other than `uv`

The `block-pip.sh` PreToolUse hook enforces this and rejects non-`uv` install
commands. If `uv` is unavailable, ask the user before proceeding.

The Python environment is `uv`-managed at the repo root (`pyproject.toml`,
`.python-version`). Run scripts via `uv run python <path>`.
