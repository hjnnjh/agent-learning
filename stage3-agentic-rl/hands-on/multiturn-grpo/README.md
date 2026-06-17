# 动手锚点 · Multi-turn Tool-use GRPO

> **目标**：用 verifiers（或 verl）端到端跑通一次**多轮工具调用**的 GRPO 训练。
> 这是阶段三的硬指标——把阶段一的 harness 当 RL 环境，credit assignment / 环境工程 /
> reward hacking 三大难点只能从端到端跑通里真正体会。

## 推荐路径

1. **首选 verifiers**：定义一个 `MultiTurnEnv` / `ToolEnv`（如带计算器或检索工具的 GSM8K），
   用 GRPOTrainer / prime-rl 启动。见 [Training 文档](https://github.com/PrimeIntellect-ai/verifiers/blob/main/docs/training.md)。
2. **备选 verl**：[Multi-turn Rollout（GSM8K 工具调用）](https://verl.readthedocs.io/en/latest/sglang_multiturn/multiturn.html) 官方端到端示例。
3. **跑代码前先读**：[Improving Multi-Turn Tool Use with RL（Bespoke Labs）](https://www.bespokelabs.ai/blog/improving-multi-turn-tool-use-with-reinforcement-learning) 看别人完整心路。

## 关注什么（学习重点）

- **Credit assignment**：长轨迹里奖励该挂在哪一轮？轨迹级 vs turn-level（读 [Turn-Level Reward Design](https://arxiv.org/abs/2505.11821)）。
- **环境工程**：rollout 怎么并行、工具执行怎么隔离/提速；retrieved-token masking 等稳定技巧。
- **Reward hacking**：弱 verifier 会规模化教坏模型（读 [Lilian Weng: Reward Hacking](https://lilianweng.github.io/posts/2024-11-28-reward-hacking/)）。

## 验收标准

1. 多轮 rollout + 工具调用能跑通，训练不崩。
2. 工具使用正确率 / 任务奖励相对基线有可见提升。
3. 能讲清环境定义、奖励设计、credit assignment 的处理方式。

## 备注

- 依赖：`uv add verifiers`（或按 verl 安装指引）。
- **不要让 Claude 自动启动训练或拉大模型/数据集**——先确认。写完可让 `harness-code-reviewer` 审阅。
- 这是长期目标，可在阶段二跑通单轮 GRPO 后再推进。
