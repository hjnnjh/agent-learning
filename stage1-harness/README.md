# 🔧 阶段一 · Agent Harness（约 3-5 周）

> 学习顺序：建立心智模型 → 徒手写最小 agent loop → 读成熟开源 harness 源码 → 学会评估 → 上下文工程进阶。
> 所有链接经 2026-06 核实。

**动手锚点**：徒手写出一个能修简单 bug 的最小 agent loop → `hands-on/min-agent-loop/`。

---

## 0. 主线课程：learn-claude-code（贯穿本阶段）

- [**learn-claude-code（shareAI-lab）**](https://github.com/shareAI-lab/learn-claude-code) · 课程/代码 — 20 课的 harness 工程系统课程，把 Claude Code 式 harness 拆成可逐课叠加的机制。核心理念：模型提供 agency，harness 给 agency 一个落地的地方；不是抄源码，而是抓住关键设计自己重建。建议与下面 1-5 节穿插推进，逐课做笔记到 `notes/`。

逐课进度打卡（s01–s20）：

- [ ] **基础（s01–s04）**：agent loop / 工具分发 / 权限 / 扩展 hooks
- [ ] **复杂任务（s05–s08）**：规划 / 委派 / 上下文管理
- [ ] **记忆与恢复（s09–s11）**：持久记忆 / 运行时 system prompt / 错误处理
- [ ] **长任务（s12–s14）**：任务图 / 后台执行 / 调度
- [ ] **协作（s15–s18）**：多 agent 团队 / 协议 / message bus / worktree 隔离
- [ ] **扩展（s19–s20）**：MCP 外部工具集成 / 综合组装

> 与本阶段映射：s01–s04 对应「徒手写 loop」，s05–s11 对应「读源码 + 上下文工程」，s12–s20 对应「长任务 harness + 多 agent」。

---

## 1. 基本概念与设计模式

- [**Building Effective Agents（Anthropic，2024.12）**](https://www.anthropic.com/engineering/building-effective-agents) · 博客 — 入门必读第一篇。区分 workflow 与 agent，讲 prompt chaining / routing / parallelization / orchestrator-worker / evaluator-optimizer，核心主张「从最简单方案开始」。
- [**How we built our multi-agent research system（Anthropic，2025.6）**](https://www.anthropic.com/engineering/multi-agent-research-system) · 博客 — orchestrator-worker 多 agent 架构实战复盘，坦诚讲子 agent 失控、token 经济学等坑。
- [**A Practical Guide to Building Agents（OpenAI，2025）**](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) · PDF — 34 页官方白皮书，与 Anthropic 那篇对照读看两家方法论异同。
- [**LLM Powered Autonomous Agents（Lilian Weng，2023.6）**](https://lilianweng.github.io/posts/2023-06-23-agent/) · 博客 — planning / memory / tool use 三组件框架，建立理论坐标系。
- [**Effective harnesses for long-running agents（Anthropic，2025.11）**](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) · 博客 — 少数直接以 harness 为主题的官方文章，进阶必读。

## 2. 徒手写最小 Agent Loop

- [**How to Build an Agent（Thorsten Ball / Amp，2025.4）**](https://ampcode.com/notes/how-to-build-an-agent) · 教程 — 「an LLM, a loop, and enough tokens」出处，约 400 行 Go 从零写出代码编辑 agent，去魅 harness 的最佳起点。
- [**Tool use with Claude（官方文档）**](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) · 文档 — tool schema、tool_use / tool_result 消息流、stop_reason 处理；配 [How tool use works](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works)。
- [**Claude Agent SDK 文档**](https://platform.claude.com/docs/en/agent-sdk/overview) · 文档 — Claude Code 同款 harness 的可编程封装；设计理念见 [Building agents with the Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)。
- [**claude-cookbooks: patterns/agents**](https://github.com/anthropics/claude-cookbooks/tree/main/patterns/agents) · 代码 — Building Effective Agents 的官方参考实现，每个模式对应一个极简 notebook。

## 3. 成熟开源 Harness 源码

- [**smolagents（Hugging Face）**](https://github.com/huggingface/smolagents) · 代码 — 核心约 1000 行，主打 CodeAgent，一天可读完；[文档](https://huggingface.co/docs/smolagents/en/index)。
- [**SWE-agent（普林斯顿）**](https://github.com/SWE-agent/SWE-agent) · 代码 — 配置驱动，学 harness 源码最佳第一站；配 [ACI 论文（NeurIPS 2024）](https://arxiv.org/abs/2405.15793)（Agent-Computer Interface 奠基论文）。
- [**OpenHands（原 OpenDevin）**](https://github.com/OpenHands/OpenHands) · 代码 — 最完整的开源软件开发 agent 平台；新版 [software-agent-sdk](https://github.com/OpenHands/software-agent-sdk) 更模块化；[平台论文（ICLR 2025）](https://arxiv.org/abs/2407.16741)。
- [**Claude Code 最佳实践文档**](https://code.claude.com/docs/en/best-practices) · 文档 — 闭源 harness 设计说明书（CLAUDE.md 注入、subagent 隔离、just-in-time 检索）。

## 4. Agent 评估

- [**SWE-bench 官网 + Leaderboard**](https://www.swebench.com/) · 榜单 — 代码 agent 评估事实标准；[GitHub](https://github.com/SWE-bench/SWE-bench)，从 Lite + Docker 起步看 [Quickstart](https://www.swebench.com/SWE-bench/guides/quickstart/)。
- [**Introducing SWE-bench Verified（OpenAI，2024.8）**](https://openai.com/index/introducing-swe-bench-verified/) · 博客 — 为什么原版 benchmark 系统性低估模型，理解「benchmark 本身也会有 bug」。
- [**Terminal-Bench**](https://www.tbench.ai/) · 榜单 — 终端环境 agent 评估金标准；[GitHub](https://github.com/laude-institute/terminal-bench)，2.0 起推荐 [Harbor 框架](https://github.com/laude-institute/harbor)。

## 5. 上下文工程（Context Engineering）

- [**Effective context engineering for AI agents（Anthropic，2025.9）**](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) · 博客 — 该领域最权威单篇：context 是有限且边际递减的资源，讲 compaction、结构化笔记、sub-agent 隔离。
- [**Managing context on the Claude Developer Platform（Anthropic，2025）**](https://www.anthropic.com/news/context-management) · 博客 — context editing + memory tool 官方发布；配 [memory tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)、[context editing](https://platform.claude.com/docs/en/build-with-claude/context-editing)。
- [**Context Engineering for AI Agents: Lessons from Building Manus**](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus) · 博客 — 生产级一线经验：KV-cache 命中率、logit masking、文件系统当外部记忆。
- [**Context Rot（Chroma Research，2025.7）**](https://research.trychroma.com/context-rot) · 报告 — 实证 18 个模型：输入越长性能越不可靠。
- [**Context Engineering for Agents（LangChain，2025.7）**](https://blog.langchain.com/context-engineering-for-agents/) · 博客 — write / select / compress / isolate 四象限框架；[配套代码](https://github.com/langchain-ai/context_engineering)。

## 建议学习路径

1. 概念：Building Effective Agents → OpenAI 指南 → Lilian Weng（理论补充）。
2. 动手：Thorsten Ball 教程（一个下午写出 loop）→ Claude tool use 文档 → cookbook patterns → **完成动手锚点**。
3. 读源码：learn-claude-code s01–s11 主线穿插 → smolagents → SWE-agent + ACI 论文 → OpenHands。
4. 评估：先读 SWE-bench Verified 博客理解坑，再用 SWE-bench Lite / terminal-bench 实际跑分。
5. 进阶：Anthropic context engineering + long-running harnesses → learn-claude-code s12–s20 → Manus 实战文 → Context Rot。
