---
name: new-note
description: 按规范模板在对应阶段的 notes/ 目录新建一篇学习笔记。当用户说「记笔记」「为某资源/论文建笔记」「写读后感」「note this」等时触发。
---

# new-note

为某个资源/论文/主题在正确的阶段 `notes/` 目录创建一篇符合 `.claude/rules/learning-notes.md`
规范的笔记。

## 步骤

1. **定位阶段**：根据资源主题判断属于哪个阶段，写入对应目录：
   - Harness / harness 工程 / 评估 / 上下文工程 / learn-claude-code → `stage1-harness/notes/`
   - RL 基础 / RLHF / DPO / GRPO / 训练框架 → `stage2-rl-posttraining/notes/`
   - Agentic RL / multi-turn / reward hacking / 环境工程 → `stage3-agentic-rl/notes/`
   - Anthropic 博客 → `stage1-harness/notes/`（与阅读清单共享）
2. **取真实链接**：从对应 `stage*/README.md` 或 `anthropic-blog/reading-list.md` 找到该资源的
   已核实 URL，**不要臆造链接**。找不到就把 `source` 留 `—` 并注明为综合笔记。
3. **取当前日期**：用真实当前日期填 `date`（必要时运行 `date +%Y-%m-%d`）。
4. **文件名**：`<kebab-case-slug>.md`，slug 取资源短名（如 `building-effective-agents.md`）。
5. **按模板写**：front-matter + 「是什么 → 为什么重要 → 关键要点 → 与动手锚点的关联 → 疑问」。
   先放骨架与已知信息；细节由用户在阅读后补全（这是学习项目，不替用户读）。
6. **更新打卡**：在对应 README / 阅读清单里把该资源的 checkbox 勾上（若用户确认已读）。

## 注意

- 这是学习项目：笔记产出帮助用户**组织**思考，不要凭空替用户总结未读内容的细节结论。
- 严格遵守 `learning-notes.md` 的 front-matter 字段与正文结构。
