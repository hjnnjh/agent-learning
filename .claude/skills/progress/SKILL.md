---
name: progress
description: 汇总三阶段动手锚点与各打卡表（阶段 README、learn-claude-code 逐课、Anthropic 三梯度阅读清单）的完成进度。当用户说「看进度」「学到哪了」「progress」「打卡情况」时触发。
---

# progress

扫描仓库，给出一份学习进度总览。

## 步骤

1. **统计 checkbox**：解析以下文件里的 `- [ ]` / `- [x]`：
   - `stage1-harness/README.md`（含 learn-claude-code s01–s20 逐课打卡）
   - `stage2-rl-posttraining/README.md`
   - `stage3-agentic-rl/README.md`
   - `anthropic-blog/reading-list.md`（三梯度）
2. **盘点笔记**：列出各 `stage*/notes/` 下已有的笔记文件数与标题。
3. **动手锚点状态**：检查三个 `hands-on/*/` 目录是否已有用户代码（非仅 README 占位），
   据此判断每个阶段的动手锚点处于「未开始 / 进行中 / 已完成」。
4. **输出**：用简体中文给一张紧凑表格（阶段 / 阅读打卡 x/总 / 笔记数 / 动手锚点状态），
   再给一句「下一步建议」（指向当前阶段尚未完成的最高优先级项）。

## 注意

- 只读取与汇总，不修改文件。
- 动手锚点是硬指标：即使阅读打卡很满，只要锚点未完成，就提示用户「别跳过动手」。
