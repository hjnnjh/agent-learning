# AGENTS.md — Operational Guidelines for AI Agents

Operational procedures and guardrails for AI agents working in the **agent-learning**
repository (a personal study project for the Notion roadmap《Agent 学习路线：Harness
与 RL 后训练》). All agents MUST adhere to these instructions.

## 1. Communication

1. **Language**: respond in Simplified Chinese (简体中文).
2. **Tone**: professional, concise, direct. State facts and tradeoffs.
3. Keep code identifiers, file paths, URLs, math notation, and tensor shapes verbatim.

## 2. Hard Guardrails (enforced by hooks)

1. **DO NOT do the user's hands-on anchors for them.** Each stage has one mandatory
   hands-on anchor (write a min agent loop / run GSM8K GRPO / run multi-turn GRPO).
   Assist, explain, and unblock — but the learner writes and runs it. Learning lives
   in the practice.
2. **DO NOT auto-run training / heavy jobs.** Ask before launching training, sweeps,
   downloading large models or datasets, or anything that consumes GPU / long wall-clock.
3. **Use `uv` only** for Python deps; `pip`/`conda install` are blocked
   (`.claude/hooks/block-pip.sh`).
4. **DO NOT auto-commit.** Never `git commit`/`git push` without explicit user
   permission. When asked, write clear, descriptive messages.
5. **Cite sources in notes.** Every note records the source link and date. Do not
   fabricate links; use the verified URLs in each stage's `README.md`.

## 3. How This Project Works

Three stages, each with three kinds of work: **read resources** (links in each
`stage*/README.md`) → **take notes** (`stage*/notes/`) → **complete the hands-on
anchor** (`stage*/hands-on/`). The Anthropic blog reading list runs in parallel
with stage 1 (`anthropic-blog/`).

Progress is tracked via the checkboxes in each stage README and the reading list.

## 4. Code (hands-on anchors, Python)

1. Follow `.claude/rules/python.md` and `python-deps.md` (auto-load by path).
2. Python env is `uv`-managed at the repo root (`pyproject.toml`, `.python-version`).
   Run via `uv run python <script>`.
3. Tensor functions document their shapes; device is resolved from config/tensor,
   never hardcoded `cuda`; eval is wrapped in `no_grad`/`eval()`.
4. After editing `.py`, the `ruff-check.sh` hook runs ruff format/check; fix what it reports.
5. Keep training reproducible: fix seeds, drive runs from config, log to W&B when training.

## 5. Notes (Markdown)

1. Follow `.claude/rules/learning-notes.md` (auto-loads for `**/notes/**/*.md`).
2. One note per resource/topic; front-matter with title, source URL, date, stage.
3. Prefer "concept → why it matters → key takeaways → open questions" structure.
4. Link related notes and the relevant hands-on anchor.

## 6. Consulting Rules Before Writing

Before substantial work, read the relevant rule files for the area you are editing
(they are short and authoritative). When uncertain about a resource link, a claim's
source, or a reproducibility detail, ask rather than guess.

End of Guidelines.
