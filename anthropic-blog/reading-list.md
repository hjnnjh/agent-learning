# 📖 Anthropic 博客精读清单（与阶段一并行）

> 工程博客 [anthropic.com/engineering](https://www.anthropic.com/engineering) 是学 agent 的核心阵地。
> 按主题分组，末尾是三梯度阅读打卡表。所有 URL 经 2026-06 核实。
> 读后笔记写进 `../stage1-harness/notes/`（与阶段一共享）。

## 内容板块概览

- [**Engineering**](https://www.anthropic.com/engineering) — 工程博客，约 25 篇，学 agent 主阵地。
- [**Research**](https://www.anthropic.com/research) — 研究成果博客版导读，通常配 arXiv 论文。
- [**News**](https://www.anthropic.com/news) — 产品发布、对齐立场文章（MCP 发布、Claude 宪法等）。
- [**Claude 文档**](https://platform.claude.com/docs/) — 提示工程、tool use 等实操指南。
- [**Transformer Circuits**](https://transformer-circuits.pub/) — 可解释性团队独立发表站，论文级深度，进阶选读。

## A. Agent 构建核心（最高优先级）

- [**Building Effective Agents**](https://www.anthropic.com/engineering/building-effective-agents)（2024-12）— 业界引用最多的 agent 入门文。
- [**How we built our multi-agent research system**](https://www.anthropic.com/engineering/multi-agent-research-system)（2025-06）— 多 agent 比单 agent 强 90.2% 但耗 15 倍 token。
- [**Building agents with the Claude Agent SDK**](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)（2025-09）— gather context → take action → verify 循环设计哲学。
- [**Effective harnesses for long-running agents**](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)（2025-11）— 长时运行 agent 的 harness 设计，做长任务必读。
- [**Equipping agents for the real world with Agent Skills**](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)（2025-10）— 文件夹 + 渐进式披露装载领域知识。

## B. Claude Code 与 Agentic Coding

- [**Claude Code: Best practices for agentic coding**](https://www.anthropic.com/engineering/claude-code-best-practices)（2025-04）— CLAUDE.md、explore-plan-code-commit、TDD、headless 模式；持续更新版见 [文档站](https://code.claude.com/docs/en/best-practices)。
- [**The "think" tool**](https://www.anthropic.com/engineering/claude-think-tool)（2025-03）— 给 Claude 一个「思考」工具在复杂 tool use 中间停下来推理。
- [**Raising the bar on SWE-bench Verified**](https://www.anthropic.com/engineering/swe-bench-sonnet)（2025-01）— 用极简 scaffold 打 SWE-bench，「把决策权交给模型」。

## C. 工具与 MCP

- [**Writing effective tools for agents — with agents**](https://www.anthropic.com/engineering/writing-tools-for-agents)（2025-09）— 给 agent 写工具的系统方法论：迭代流程、命名空间、token 效率。
- [**Introducing the Model Context Protocol**](https://www.anthropic.com/news/model-context-protocol)（2024-11）— MCP 发布，「AI 的 USB-C」。
- [**Code execution with MCP**](https://www.anthropic.com/engineering/code-execution-with-mcp)（2025-11）— 让 agent 写代码调 MCP 而非直接塞工具定义，省 98.7% token。
- [**Introducing advanced tool use**](https://www.anthropic.com/engineering/advanced-tool-use)（2025-11）— Tool Search、programmatic tool calling 等进阶机制。

## D. Context Engineering 与提示工程

- [**Effective context engineering for AI agents**](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)（2025-09）— 注意力预算、compaction、结构化笔记、sub-agent 隔离。
- [**Prompt engineering overview（文档）**](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview) — 官方提示工程指南入口。
- [**System Prompts 发布记录**](https://docs.anthropic.com/en/release-notes/system-prompts) — 官方公开真实 system prompt，逆向学习一手素材。
- [**Introducing Contextual Retrieval**](https://www.anthropic.com/engineering/contextual-retrieval)（2024-09）— 为每个 chunk 生成上下文说明再嵌入，检索失败率降 49%。

## E. 评估（Evals）

- [**Demystifying evals for AI agents**](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)（2026-01）— 从抽查到自动化 grader、pass@k、避免 eval 腐烂。
- [**Designing AI-resistant technical evaluations**](https://www.anthropic.com/engineering/AI-resistant-technical-evaluations)（2026-01）— 设计模型作弊不了的技术评测。

## F. 对齐 / RL / 研究

- [**Constitutional AI: Harmlessness from AI Feedback**](https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback)（2022-12）— RLAIF 开山之作；[论文](https://arxiv.org/abs/2212.08073)。
- [**Claude's Constitution**](https://www.anthropic.com/news/claudes-constitution)（2025-01）— 逐条解释；新版（2026-01）见 [Claude's new constitution](https://www.anthropic.com/news/claude-new-constitution)。
- [**Collective Constitutional AI**](https://www.anthropic.com/research/collective-constitutional-ai-aligning-a-language-model-with-public-input)（2023-10）— 公众投票起草宪法并训练。
- [**Core Views on AI Safety**](https://www.anthropic.com/news/core-views-on-ai-safety)（2023-03）— Anthropic 安全世界观总纲。

## G. 可解释性（进阶选读）

- [**Tracing the thoughts of a large language model**](https://www.anthropic.com/research/tracing-thoughts-language-model)（2025-03）— 科普版导读，从这篇读起。
- [**Mapping the Mind of a Large Language Model**](https://www.anthropic.com/research/mapping-mind-language-model)（2024-05）— 稀疏自编码器提取数百万可解释特征。
- 深入原文：[On the Biology of a Large Language Model](https://transformer-circuits.pub/2025/attribution-graphs/biology.html)、[Toy Models of Superposition](https://transformer-circuits.pub/2022/toy_model/index.html)、[A Mathematical Framework for Transformer Circuits](https://transformer-circuits.pub/2021/framework/index.html)。

---

## 三梯度阅读打卡表

### 梯度 1 — 工程实践（先建立直觉，约 1 周）
- [ ] Building Effective Agents
- [ ] Claude Code: Best practices
- [ ] Effective context engineering for AI agents
- [ ] Writing effective tools for agents
- [ ] Prompt engineering 文档 overview

### 梯度 2 — 系统设计与规模化（约 1-2 周）
- [ ] How we built our multi-agent research system
- [ ] Building agents with the Claude Agent SDK
- [ ] MCP 发布文 + Code execution with MCP
- [ ] Effective harnesses for long-running agents
- [ ] Demystifying evals for AI agents
- [ ] 穿插选读：think tool、Agent Skills、Contextual Retrieval

### 梯度 3 — 研究与对齐（理解「为什么」，节奏自定）
- [ ] Core Views on AI Safety
- [ ] Constitutional AI 导读（有余力读 arXiv 原文）
- [ ] Claude's Constitution
- [ ] Tracing the thoughts + Mapping the Mind
- [ ] 进阶：transformer-circuits.pub 原文
