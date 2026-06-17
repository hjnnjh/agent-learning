---
type: "auto"
globs: ["**/*.py"]
---

# Python Code Style (hands-on anchors)

> **Applicable files**: all `*.py` (mainly under `stage*/hands-on/`).

## Key Principles

1. Readability first; keep it simple; minimal example that satisfies the goal.
2. Comments explain intent ("why"), not restate code ("what").
3. All comments and docstrings in code MUST be in English.
4. Do NOT add extra blank lines inside classes/methods/functions.
5. Do NOT add logging/print statements unless explicitly requested or needed to
   observe a training signal (e.g. reward curve) — for learning, observing is fine.
6. Do NOT wrap code in `try...except` unless an error is genuinely expected.
7. Do NOT leave commented-out dead code; delete it.

## Naming & Formatting

- `snake_case` functions/variables, `PascalCase` classes, `UPPER_SNAKE_CASE` constants.
- Tensor variables carry semantics (`event_emb`, `attn_weights`), not bare `x`/`y`.
- 4-space indent; line width <= 88 (ruff `line-length = 88`).
- Imports: stdlib -> third-party -> local, blank line between groups; no wildcard imports.

## Type Annotations & Docstrings

- Annotate all function parameters and return values.
- Triple-quoted docstrings for module/class/public function.
- For modeling/training code, the docstring states input/output tensor shapes.

## Reproducibility (training scripts)

- Fix seeds (`torch`, `numpy`, `random`); drive runs from a config, not hardcoded magic numbers.
- Resolve device from config/tensor; never hardcode `cuda`.
- Wrap evaluation in `torch.no_grad()` and `model.eval()`.
- Dependencies installed via `uv` only (see `python-deps.md`).
