# Claude Code 配置模块

本模块定义 **agent-learning** 项目的 Claude Code 工作流配置。配置范式参考
[RQ-TPP](https://github.com/hjnnjh/RQ-TPP)。规则与技能的具体内容请直接阅读对应文件，此处仅做索引。

## 目录结构

```
.claude/
├── CLAUDE.md                 # 本文档（索引）
├── settings.json             # 团队级 hooks
├── rules/                    # 自动加载规则（按 globs 匹配文件）
├── skills/                   # 项目技能
├── agents/                   # 子智能体
└── hooks/                    # 工作流钩子
```

## 规则（Rules）

规则按 `globs` 自动匹配并加载，无需手动调用。

| 规则 | 作用域 | 一句话说明 |
|---|---|---|
| `python.md` | `**/*.py` | 严格 Python 风格：88 行宽、英文注释、类型注解、禁多余空行/print/try |
| `python-deps.md` | 全局 | 强制 `uv` 安装依赖，禁 pip/conda |
| `learning-notes.md` | `**/notes/**/*.md` | 笔记格式：front-matter（来源/日期/阶段）、概念→为何重要→要点→疑问 |
| `language.md` | 全局 | 简体中文回复、术语准确、客观简洁 |

## 技能（Skills）

通过自然语言或 `/技能名` 触发。

| 技能 | 描述 |
|---|---|
| `new-note` | 按规范模板在对应阶段 `notes/` 新建一篇资源/论文学习笔记 |
| `progress` | 汇总三阶段动手锚点与各打卡表的完成进度 |

## 子智能体（Agents）

| 名称 | 描述 |
|---|---|
| `paper-reader` | 精读一篇论文/技术报告并产出结构化笔记（贡献、方法、结果、局限、与路线的关联） |
| `harness-code-reviewer` | 审阅动手锚点代码（agent loop / 训练脚本）：loop 正确性、工具协议、数值稳定、可复现 |

## 工作流钩子（Hooks）

在 `settings.json` 中配置。

| Hook | 触发时机 | 描述 |
|---|---|---|
| `block-pip.sh` | PreToolUse(Bash) | 拦截 pip/pip3/conda install，强制 `uv` |
| `ruff-check.sh` | PostToolUse(Write/Edit) | 对 `.py` 自动运行 ruff format/check（若已安装 ruff） |

## 与 RQ-TPP 的差异

本项目是**学习型**而非论文研究型，故去掉了 LaTeX / OpenSpec / W&B / 审稿相关的规则与技能，
保留并适配了：Python 风格、uv 依赖护栏、简体中文、ruff 钩子，新增了「学习笔记规范」与
「论文精读 / 代码审阅」子智能体。最大护栏是 **不替用户完成动手锚点**（见 `AGENTS.md` §2）。
