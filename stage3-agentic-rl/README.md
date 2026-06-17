# 🤖 阶段三 · Agentic RL（两条线汇合，长期）

> 2025 年以来最热的方向：把阶段一的 harness 当作 RL 环境训练多轮 agent。
> 路径：综述 + reward hacking 建立认知 → 用 verifiers 跑通 multi-turn GRPO → 精读三个代表作 → 系统类文章理解规模化基建。
> 所有链接经 2026-06 核实。

**三大难点**：credit assignment（长轨迹哪一步该奖励）、环境工程（沙箱要快且可并行）、reward hacking。

**动手锚点**：用 verifiers 或 verl 端到端跑通一次 multi-turn tool-use GRPO → `hands-on/multiturn-grpo/`。

---

## 1. 综述与认知建立

- [**The Landscape of Agentic RL for LLMs: A Survey**](https://arxiv.org/abs/2509.02547) · 论文 — 最系统的 Agentic RL 综述：单步 MDP 与长时序 POMDP 的正式对比，首选入口。
- [**A Comprehensive Survey on RL-based Agentic Search**](https://arxiv.org/abs/2510.16724) · 论文 — 聚焦「RL 训练搜索 agent」这个最成熟子方向。
- [**Reinforcing Multi-Turn Reasoning via Turn-Level Reward Design（NeurIPS 2025）**](https://arxiv.org/abs/2505.11821) · 论文 — 直击多轮 RL 的 credit assignment：轨迹级稀疏奖励失效与 turn-level reward 的 MDP 重构。
- [**Verlog: A Multi-turn RL framework for LLM agents（CMU ML Blog）**](https://blog.ml.cmu.edu/2025/09/15/verlog-a-multi-turn-rl-framework-for-llm-agents/) · 博客 — 长 horizon、回合长度可变场景下的多轮 RL 工程与算法。
- [**Multi-Turn Credit Assignment with LLM Agents（hlfshell）**](https://hlfshell.ai/posts/multi-turn-credit-assignment/) · 博客 — 通俗梳理 + 文献串讲，快速建立问题直觉。

## 2. 环境与框架

- [**verifiers（Will Brown / Prime Intellect）**](https://github.com/PrimeIntellect-ai/verifiers) · 代码 — 模块化 RL 环境/评测库，MultiTurnEnv / ToolEnv 抽象，社区事实标准，**强烈建议第一个上手**；[文档](https://docs.primeintellect.ai/verifiers)、[Training 专题](https://github.com/PrimeIntellect-ai/verifiers/blob/main/docs/training.md)。
- [**Prime Intellect Environments Hub**](https://www.primeintellect.ai/blog/environments) · 平台 — 「RL 环境的 GitHub」，可直接拉别人的环境训练/评测；[Hub 入口](https://app.primeintellect.ai/dashboard/environments)。
- [**prime-rl**](https://github.com/PrimeIntellect-ai/prime-rl) · 代码 — 大规模异步 RL 训练器，与 verifiers 原生对接。
- [**SkyRL（NovaSky / Berkeley）**](https://github.com/NovaSky-AI/SkyRL) · 代码 — 全栈模块化 RL 库：skyrl-train / skyrl-gym / skyrl-agent；[SkyRL-Agent 论文](https://arxiv.org/abs/2511.16108)。
- [**verl 的 Agentic RL 支持**](https://verl.readthedocs.io/en/latest/start/agentic_rl.html) · 文档 — v0.4.2 起 Agent Loop 抽象，基于 SGLang 多轮 rollout + 自定义工具；[Multi-turn rollout 文档](https://verl.readthedocs.io/en/latest/sglang_multiturn/multiturn.html)。
- [**rLLM（Agentica）**](https://github.com/rllm-org/rllm) · 代码 — 面向自定义 agent + 环境的后训练框架，DeepSWE、DeepScaleR 用它训出。

## 3. 代表性工作 / 论文

- [**Search-R1**](https://arxiv.org/abs/2503.09516) · 论文 — 搜索 agent RL 开山之作（基于 verl）：多轮检索交织推理、retrieved-token masking、纯 outcome reward，最常被复刻；[代码](https://github.com/PeterGriffinJin/Search-R1)。
- [**SWE-RL（Meta）**](https://arxiv.org/abs/2502.18449) · 论文 — 首个把 RL 规模化用于真实软件工程：GitHub PR 演化数据 + 轻量规则奖励；[代码](https://github.com/facebookresearch/swe-rl)。
- [**DeepSWE（Agentica × Together）**](https://www.together.ai/blog/deepswe) · 博客 — 用 rLLM 在 4500 真实 SWE 任务上纯 RL 训 Qwen3-32B，配方/消融/踩坑全公开。
- [**Kimi-Researcher（Moonshot）**](https://moonshotai.github.io/Kimi-Researcher/) · 报告 — 端到端 agentic RL 标杆：全异步 rollout 系统、turn-level partial rollout。
- [**Kimi K2: Open Agentic Intelligence**](https://arxiv.org/abs/2507.20534) · 报告 — agentic 数据合成 + Gym 风格统一环境接口 + partial rollout。
- [**rStar2-Agent（Microsoft）**](https://arxiv.org/abs/2508.20722) · 报告 — 14B 模型靠 agentic RL（代码工具环境 + GRPO 改进 + 高吞吐隔离执行）达前沿数学推理。

## 4. 实践教程（端到端跑通 multi-turn GRPO → 即本阶段动手锚点）

- [**verifiers Training 文档 + 环境示例**](https://github.com/PrimeIntellect-ai/verifiers/blob/main/docs/training.md) · 文档 — 从定义 MultiTurnEnv/工具环境到用 GRPOTrainer / prime-rl 启动训练，最短路径。
- [**verl Multi-turn Rollout（GSM8K 工具调用）**](https://verl.readthedocs.io/en/latest/sglang_multiturn/multiturn.html) · 教程 — 官方端到端：数据预处理 → 配 YAML 工具 → 开启 multi_turn rollout；另有 [搜索工具集成示例](https://verl.readthedocs.io/en/latest/sglang_multiturn/search_tool_example.html)。
- [**Improving Multi-Turn Tool Use with RL（Bespoke Labs）**](https://www.bespokelabs.ai/blog/improving-multi-turn-tool-use-with-reinforcement-learning) · 博客 — 用 GRPO 提升小模型多轮工具调用的完整实验（奖励设计、曲线、失败分析），跑代码前先看。
- [**ms-swift Multi-turn GRPO 开发指南**](https://swift.readthedocs.io/en/latest/Instruction/GRPO/DeveloperGuide/multi_turn.html) · 文档 — ModelScope swift 多轮 GRPO，中文生态友好，verl 之外备选。

## 5. 难点专题：Reward Hacking 与环境工程

- [**Reward Hacking in RL（Lilian Weng，2024.11）**](https://lilianweng.github.io/posts/2024-11-28-reward-hacking/) · 博客 — reward hacking 最权威综述长文，奖励设计前必读。
- [**How to Design our Agentic RL Systems?（Jiachen Liu）**](https://amberljc.github.io/blog/2025-09-05-agentic-rl-systems.html) · 博客 — 系统视角：Agent Layer 解耦训练与执行、统一轨迹格式、远程执行池、异步流水线。
- [**Running RL agents in secure sandboxes（Northflank）**](https://northflank.com/blog/reinforcement-learning-agents-in-secure-sandboxes) · 博客 — 数千并发环境的沙箱选型（Firecracker/Kata microVM vs gVisor）。
- [**A Taxonomy of RL Environments for LLM Agents（Hanchung Lee）**](https://leehanchung.github.io/blogs/2026/03/21/rl-environments-for-llm-agents/) · 博客 — 环境分类学，把环境质量与 reward hacking 联系起来。
- [**Environment Scaling for Interactive Agentic Experience Collection: A Survey**](https://arxiv.org/pdf/2511.09586) · 论文 — 如何规模化构造交互式训练环境。
