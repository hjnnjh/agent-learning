# 🧭 Agent 学习路线：Harness 与 RL 后训练

学习型项目。承载 Notion 路线《Agent 学习路线：Harness 与 RL 后训练》的资料、笔记与动手锚点。
配置范式参考 [RQ-TPP](https://github.com/hjnnjh/RQ-TPP)（规则自动加载 / 技能按需触发 / 子智能体 / hooks 护栏）。

> **怎么用这个仓库**：按阶段推进，每个阶段做完对应的「动手锚点」再进入下一阶段——只读不写在这个领域几乎学不到东西。
> 资料链接在各 `stage*/README.md`（均经 2026-06 核实），笔记写进 `stage*/notes/`，动手代码写进 `stage*/hands-on/`。

## 核心认知

Harness 与 RL 后训练是同一件事的两面：

- **Harness（推理时）**：让模型把活干好的脚手架——工具调用循环、上下文管理、子 agent 编排、评估体系。
- **RL 后训练（训练时）**：让模型本身变强的方法——SFT → 偏好优化（DPO）→ RLVR（GRPO 等可验证奖励 RL）。
- 两条线最终在 **Agentic RL** 汇合：把 harness 当作 RL 环境，对多轮工具调用轨迹做强化学习。

## 路线图

| 阶段 | 主题 | 周期 | 动手锚点 |
|---|---|---|---|
| [阶段一](stage1-harness/README.md) | Agent Harness | 约 3-5 周 | 徒手写出一个能修简单 bug 的最小 agent loop |
| [阶段二](stage2-rl-posttraining/README.md) | RL 后训练 | 约 6-10 周 | 用 TRL 在 Qwen 小模型上跑通 GSM8K GRPO，看到奖励曲线上升 |
| [阶段三](stage3-agentic-rl/README.md) | Agentic RL | 长期 | 用 verifiers/verl 端到端跑通 multi-turn tool-use GRPO |
| [并行](anthropic-blog/reading-list.md) | Anthropic 博客精读 | 与阶段一同步 | 三梯度阅读打卡（工程实践 → 系统设计 → 研究对齐） |

## 主线课程（贯穿阶段一）

- **[learn-claude-code（shareAI-lab）](https://github.com/shareAI-lab/learn-claude-code)** — 20 课的 harness 工程系统课程（s01–s20）：
  从 agent loop / 工具分发 / 权限，到上下文压缩、子 agent、任务图、多 agent 协作、MCP 集成。
  核心主张「Agency comes from the model. The harness gives agency a place to land.」——
  不是抄源码，而是抓住关键设计自己重建，是阶段一「读成熟 harness」与「上下文工程」的最佳骨架课程。
  阶段一 README 含逐课进度打卡表。

## 学习建议

- **可以并行**：阶段一的「徒手写 loop」和阶段二的「RL 基础」互不依赖；Anthropic 博客精读与阶段一同步。
- **资源比例**：博客和开源代码比教科书重要，论文以技术报告为主、理论文章为辅。
- **长期订阅**：Interconnects（Nathan Lambert）、Ahead of AI（Sebastian Raschka）、Lil'Log（Lilian Weng）。
- **最重要的一条**：每个阶段都有一个必须完成的动手锚点，大量知识（上下文管理的坑、rollout 工程细节、
  reward hacking 的具体形态）只存在于实践中。

## 环境

- 笔记：纯 Markdown，无需环境。
- 动手代码（阶段二/三）：Python，`uv` 管理（见根 `pyproject.toml`）。`uv venv && uv sync` 起步。

配置说明见 [CLAUDE.md](CLAUDE.md) 与 [.claude/CLAUDE.md](.claude/CLAUDE.md)。
