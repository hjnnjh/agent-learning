# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> **agent-learning**：一个**学习型项目**，用于系统学习 Notion 路线《Agent 学习路线：Harness 与 RL 后训练》。
> 三个阶段（Harness → RL 后训练 → Agentic RL）各有「读资料 + 记笔记 + 动手锚点」三类工作，
> 配置范式参考 [RQ-TPP](https://github.com/hjnnjh/RQ-TPP)：规则按路径自动加载、技能按需触发、子智能体处理专项、hooks 强制护栏。

## 项目结构

```
agent-learning/
├── stage1-harness/            # 阶段一 · Agent Harness（约 3-5 周）
│   ├── README.md              #   资源详单 + 学习路径
│   ├── notes/                 #   读书/读源码笔记
│   └── hands-on/min-agent-loop/   # 动手锚点：徒手写最小 agent loop（能修简单 bug）
├── stage2-rl-posttraining/    # 阶段二 · RL 后训练（约 6-10 周）
│   ├── README.md
│   ├── notes/
│   └── hands-on/grpo-gsm8k/   # 动手锚点：TRL 在 Qwen 小模型上跑通 GSM8K GRPO
├── stage3-agentic-rl/         # 阶段三 · Agentic RL（两条线汇合，长期）
│   ├── README.md
│   ├── notes/
│   └── hands-on/multiturn-grpo/   # 动手锚点：verifiers/verl 端到端 multi-turn tool-use GRPO
├── anthropic-blog/            # Anthropic 博客精读打卡表（与阶段一并行）
├── .claude/                   # Claude Code 配置（rules/skills/agents/hooks，详见 .claude/CLAUDE.md）
├── AGENTS.md                  # 通用 AI 操作铁律
├── pyproject.toml             # Python 环境（uv 管理，阶段二/三动手用）
└── CLAUDE.md                  # 本文档
```

## 核心认知（来自路线总览）

Harness 与 RL 后训练是同一件事的两面：

- **Harness（推理时）**：让模型把活干好的脚手架——工具调用循环、上下文管理、子 agent 编排、评估体系。
- **RL 后训练（训练时）**：让模型本身变强的方法——SFT → 偏好优化（DPO）→ RLVR（GRPO 等可验证奖励 RL）。
- 两条线在 **Agentic RL** 汇合：把 harness 当作 RL 环境，对多轮工具调用轨迹做强化学习。

## 关键约束（务必遵守）

1. **以「学懂」为目标，不要替用户跳过动手环节**：每个阶段的动手锚点必须由用户亲手完成，Claude 协助而非代劳；大量知识只存在于实践中。
2. **Python 依赖只用 `uv`**：禁止 `pip`/`conda install`（`.claude/hooks/block-pip.sh` 已强制拦截）。
3. **不要自动跑训练/重任务**：训练、sweep、下载大模型/数据集等耗 GPU 或长时操作前先征求同意。
4. **不要自动提交 git**：commit/push 必须经用户明确同意。
5. **笔记可追溯**：每篇笔记标注来源链接与日期；资源链接以各阶段 `README.md` 为准（均经 2026-06 核实）。

## 常用命令

```bash
# Python 环境（阶段二/三动手时，在项目根用 uv）
uv venv && uv sync                       # 或 uv pip install -e .
uv run python stage2-rl-posttraining/hands-on/grpo-gsm8k/train.py

# 安装依赖（强制 uv）
uv add <package>
```

## 规则与技能

规则按文件路径自动加载（`.claude/rules/`），技能按需触发（`.claude/skills/`），
子智能体处理专项任务（`.claude/agents/`）。完整索引见 `.claude/CLAUDE.md`。

## 学习建议

- **可以并行**：阶段一的「徒手写 loop」与阶段二的「RL 基础」互不依赖；Anthropic 博客精读与阶段一同步。
- **资源比例**：本领域博客和开源代码比教科书重要，论文以技术报告为主。
- **长期订阅**：Interconnects（Nathan Lambert）、Ahead of AI（Sebastian Raschka）、Lil'Log（Lilian Weng）。
