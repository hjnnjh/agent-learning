# 动手锚点 · GSM8K GRPO

> **目标**：用 TRL 在一个 Qwen 小模型上跑通一次 GSM8K 的 GRPO 训练，**看到奖励曲线上升**。
> 这是阶段二的硬指标——RLVR 的全流程直觉（奖励函数、组内相对优势、KL 约束）只能从跑通里得到。

## 推荐路径（按门槛从低到高）

1. **无卡/小卡起步**：[Unsloth GRPO 教程](https://unsloth.ai/docs/get-started/reinforcement-learning-rl-guide/tutorial-train-your-own-reasoning-model-with-grpo) — 免费 Colab 16GB（最低 5GB VRAM）。
2. **单文件读懂全流程**：[Will Brown grpo_demo gist](https://gist.github.com/willccbb/4676755236bb08cab5f4e54a0475d6fb) — Qwen2.5 + GSM8K，几百行。
3. **官方接口**：[TRL GRPO Trainer 文档](https://huggingface.co/docs/trl/main/en/grpo_trainer) + [HF LLM Course Ch.12](https://huggingface.co/learn/llm-course/chapter12/4)。

## 关注什么（学习重点）

- **奖励函数设计**：答案正确性奖励 + 格式奖励；想想哪里可能被 reward hacking。
- **GRPO 机制**：去掉 critic、组内相对优势怎么算；组大小、KL 系数、clip 的影响。
- **训练信号**：reward / KL / completion length 曲线怎么读；上升≠学好，警惕崩溃与刷格式分。

## 验收标准

1. 训练能跑完若干步且不崩。
2. 奖励曲线（或正确率）相对基线有可见上升。
3. 能对着曲线说清「为什么涨/为什么停/有没有 hack」。

## 备注

- 依赖：`uv add trl transformers datasets`（按教程；vLLM/加速按需）。
- **不要让 Claude 自动启动训练**——耗 GPU/长时操作先确认。写完脚本可让 `harness-code-reviewer` 审阅。
- 训练记录建议接 W&B 看曲线。
