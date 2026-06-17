---
type: "auto"
globs: ["**/notes/**/*.md", "**/notes/*.md"]
---

# Learning Notes Convention

> **Applicable files**: all Markdown under any `notes/` directory.

Every note is **one resource or one topic**. Keep notes traceable and skimmable.

## Front-matter (required)

```markdown
---
title: <resource or topic title>
source: <the verified URL from the stage README, or "—" for synthesis notes>
type: blog | paper | doc | course | code
stage: 1 | 2 | 3 | anthropic-blog
date: YYYY-MM-DD          # date you read it (use the real current date)
---
```

## Body structure (recommended)

1. **是什么 / 一句话** — the core claim in one sentence.
2. **为什么重要** — where it sits in the roadmap, what problem it addresses.
3. **关键要点** — bullet takeaways; quote exact terms/APIs/shapes verbatim.
4. **与动手锚点的关联** — how this informs the stage's hands-on anchor.
5. **疑问 / 待办** — open questions to chase later; link related notes `[[note-name]]`.

## Rules

- Do NOT fabricate URLs or claims. If a fact isn't in the source, mark it as your
  inference. Prefer linking the stage `README.md` entry over re-pasting a URL.
- Keep one idea per sentence; Simplified Chinese prose is fine, but keep technical
  terms, code identifiers, and math notation verbatim.
- Update the relevant checkbox in the stage `README.md` (or reading list) when done.
