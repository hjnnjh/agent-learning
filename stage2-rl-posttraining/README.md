# 🏋️ 阶段二 · RL 后训练（约 6-10 周）

> 学习顺序：RL 最小必要基础 → 系统教材 → 论文线 → 框架实战。所有链接经 2026-06 核实。

**动手锚点**：用 TRL 在 Qwen 小模型上跑通一次 GSM8K GRPO，看到奖励曲线上升 → `hands-on/grpo-gsm8k/`。

---

## 1. RL 基础（面向 LLM 的最小必要集）

- [**OpenAI Spinning Up in Deep RL**](https://spinningup.openai.com/en/latest/) · 课程 — RL 入门事实标准；只需读 Intro 三部曲 + PPO 部分。
- [**Sutton & Barto《Reinforcement Learning: An Introduction》第二版**](http://incompleteideas.net/book/the-book-2nd.html) · 书（免费 PDF） — RL 圣经，选读 MDP、策略梯度章节当理论底座。
- [**Policy Gradient Algorithms（Lilian Weng）**](https://lilianweng.github.io/posts/2018-04-08-policy-gradient/) · 博客 — 一篇串起 REINFORCE → Actor-Critic → TRPO → PPO 的完整推导链。
- [**The 37 Implementation Details of PPO**](https://iclr-blog-track.github.io/2022/03/25/ppo-implementation-details/) · 博客 — PPO 论文没写但决定成败的 37 个实现细节；[配套代码](https://github.com/vwxyzjn/ppo-implementation-details)。
- [**HuggingFace Deep RL Course Unit 8（PPO）**](https://huggingface.co/learn/deep-rl-course/en/unit8/introduction) · 课程 — 用 CleanRL 从零手写 PPO，免费 Colab 可跑。

## 2. RLHF / 后训练系统教材

- [**RLHF Book（Nathan Lambert）**](https://rlhfbook.com/) · 书 — 唯一系统覆盖后训练全栈的教科书（SFT → RM → 拒绝采样 → RL → DPO → RLVR → 评测），**本阶段主线教材**；[PDF](https://rlhfbook.com/book.pdf)、[课程](https://rlhfbook.com/course)。
- [**HuggingFace Alignment Handbook**](https://github.com/huggingface/alignment-handbook) · 代码 — HF 官方对齐配方库（Zephyr、SmolLM3 等完整可复现 recipe）。
- [**HuggingFace smol-course**](https://github.com/huggingface/smol-course) · 课程 — 最小后训练课程，本地小模型可跑，GPU 要求极低；[在线版](https://huggingface.co/learn/smol-course/unit0/1)。
- [**UC Berkeley CS285（Sergey Levine）**](https://rail.eecs.berkeley.edu/deeprlcourse/) · 课程 — 深度 RL 经典研究生课，选看 policy gradient / actor-critic 及 RLHF 讲次。
- [**Post-training of LLMs（DeepLearning.AI × Banghua Zhu）**](https://www.deeplearning.ai/courses/post-training-of-llms) · 短课 — 几小时过完 SFT/DPO/在线 RL 的 hands-on。

## 3. 关键论文线（按演进顺序）

1. [**InstructGPT**](https://arxiv.org/abs/2203.02155) — RLHF 三段式（SFT → RM → PPO）奠基之作。
2. [**DPO: Direct Preference Optimization**](https://arxiv.org/abs/2305.18290) — 把 RLHF 化简为分类损失，免去 RM 和 PPO。
3. [**DeepSeekMath（GRPO 提出）**](https://arxiv.org/abs/2402.03300) — GRPO 出处：去 critic、用组内相对优势（只看 GRPO 章节即可）。
4. [**DeepSeek-R1**](https://arxiv.org/abs/2501.12948) — 纯 RL（RLVR）激发推理能力的里程碑，「aha moment」出处。
5. [**Tülu 3（Ai2）**](https://arxiv.org/abs/2411.15124) — 最透明的全开源后训练配方（SFT+DPO+RLVR），首次系统提出 RLVR。
6. [**Kimi k1.5**](https://arxiv.org/abs/2501.12599) — RL scaling 报告，long-CoT/short-CoT 与长度控制视角。
7. [**Qwen3 Technical Report**](https://arxiv.org/abs/2505.09388) — 一线开源模型完整后训练流水线（含 RL 阶段与思考预算）。

## 4. 训练框架实战

### TRL（入门首选）
- [**TRL**](https://github.com/huggingface/trl) · 代码 — HF 官方 RL 训练库，PPO/DPO/GRPO trainer 齐全，小规模实验首选。
- [**GRPO Trainer 官方文档**](https://huggingface.co/docs/trl/main/en/grpo_trainer) · 文档 — GRPO 参数、奖励函数接口、vLLM 加速。
- [**HF LLM Course Ch.12：Implementing GRPO in TRL**](https://huggingface.co/learn/llm-course/chapter12/4) · 课程 — 手把手在 TRL 里写 GRPO。

### 小模型跑 GSM8K GRPO（强烈推荐先做这个 → 即本阶段动手锚点）
- [**Will Brown 的 grpo_demo gist**](https://gist.github.com/willccbb/4676755236bb08cab5f4e54a0475d6fb) · 代码 — 最著名的单文件 GRPO 脚本：Qwen2.5 小模型 + GSM8K，几百行看懂 RLVR 全流程。
- [**Mini-R1（Phil Schmid）**](https://www.philschmid.de/mini-deepseek-r1) · 博客 + [notebook](https://github.com/philschmid/deep-learning-pytorch-huggingface/blob/main/training/mini-deepseek-r1-aha-grpo.ipynb) — GRPO + Countdown 复现 R1 的 aha moment。
- [**Unsloth GRPO 教程**](https://unsloth.ai/docs/get-started/reinforcement-learning-rl-guide/tutorial-train-your-own-reasoning-model-with-grpo) · Colab — 免费 16GB Colab 即可跑（最低 5GB VRAM），无卡党最低门槛。

### verl（生产级，社区主阵地）
- [**verl**](https://github.com/volcengine/verl) · 代码 — HybridFlow 开源实现，支持 PPO/GRPO/DAPO/REINFORCE++，可扩展到 70B+；重点理解 rollout 引擎（vLLM/SGLang）与训练引擎（FSDP/Megatron）的解耦。
- [**verl Quickstart：GSM8K PPO**](https://verl.readthedocs.io/en/latest/start/quickstart.html) · 文档 — 24GB 显存即可；另有 [GSM8K 示例详解](https://verl.readthedocs.io/en/latest/examples/gsm8k_example.html)。

### OpenRLHF
- [**OpenRLHF**](https://github.com/OpenRLHF/OpenRLHF) · 代码 — Ray + vLLM + ZeRO-3，直接吃 HF checkpoint，PPO/REINFORCE++/GRPO 一个 flag 切换；[文档](https://openrlhf.readthedocs.io/)。

> 实战路径：TRL + Will Brown gist / Unsloth（单卡入门）→ Mini-R1（多卡）→ verl 或 OpenRLHF（规模化/研究）。

## 5. 跟踪渠道

- [**Interconnects（Nathan Lambert）**](https://www.interconnects.ai/) · newsletter — 跟踪 post-training 信噪比最高的单一信源。
- [**Ahead of AI（Sebastian Raschka）**](https://magazine.sebastianraschka.com/) · newsletter — 其 [The State of RL for LLM Reasoning](https://magazine.sebastianraschka.com/p/the-state-of-llm-reasoning-model-training) 可当导读。
- [**GRPO 详解（Cameron Wolfe）**](https://cameronrwolfe.substack.com/p/grpo) · 博客 — 逐公式拆解，配 DeepSeekMath 论文读。
- [**Lil'Log RL 标签页**](https://lilianweng.github.io/tags/reinforcement-learning/) · 博客 — 每篇都是领域级综述。
