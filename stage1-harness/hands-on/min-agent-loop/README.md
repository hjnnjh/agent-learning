# 动手锚点 · 最小 Agent Loop（s01，DeepSeek）

> **目标**：不用任何 agent 框架，直接用原生 LLM API 写一个 `while` 循环，给它一个 **bash** 工具，
> 让它能自主行动（读文件 → 定位 → 修复 → 跑测试确认）。对照 learn-claude-code
> [s01_agent_loop](https://github.com/shareAI-lab/learn-claude-code/tree/main/s01_agent_loop)。
> 这是阶段一的硬指标——大量 harness 直觉只能从这里得到。

## 当前进度

脚手架已备好（DeepSeek / OpenAI 兼容端点）：

| 文件 | 状态 | 说明 |
|---|---|---|
| `.env.example` | ✅ | 复制成 `.env` 并填 DeepSeek key |
| `check_api.py` | ✅ | 连通性自测（单轮对话，无工具） |
| `code.py` | 🚧 | client / 工具定义 / `run_bash` / CLI 已就绪，**核心 `agent_loop` 留你手写** |

## 准备（已完成）

依赖已通过 `uv` 装好（`openai` + `python-dotenv`，在仓库根 `pyproject.toml`）。

```sh
# 1) 在项目根创建 .env（已被 .gitignore 忽略，不会入库）
cp stage1-harness/hands-on/min-agent-loop/.env.example \
   stage1-harness/hands-on/min-agent-loop/.env
# 2) 编辑 .env，填入 DEEPSEEK_API_KEY（控制台：https://platform.deepseek.com/api_keys）
# 3) 验证连通性（应打印 reply='pong' 与 usage）
cd stage1-harness/hands-on/min-agent-loop && uv run python check_api.py
```

> 模型用 `deepseek-chat`（支持函数调用）。**不要用 `deepseek-reasoner`**——它不支持工具调用。

## 你要写的（动手锚点本体）

打开 `code.py`，实现 `agent_loop(messages)`，把这 5 步翻译成代码（DeepSeek / OpenAI 语义）：

```text
while True:
    1. resp = client.chat.completions.create(model=MODEL, messages=messages, tools=TOOLS)
    2. msg = resp.choices[0].message;  messages.append(msg)
    3. if resp.choices[0].finish_reason != "tool_calls":  return     # 模型做完了
    4. for call in msg.tool_calls:                                    # 可能不止一个
         args = json.loads(call.function.arguments)
         out  = run_bash(args["command"])
         messages.append({"role": "tool", "tool_call_id": call.id, "content": out})
    5. （回到 while 顶部）
```

与 s01 官方 Anthropic 版的对应：`stop_reason == "tool_use"` ↔ `finish_reason == "tool_calls"`；
`tool_result` 块 ↔ `{"role": "tool", ...}` 消息。自己翻译一遍，正是这一课的价值。

运行：

```sh
cd stage1-harness/hands-on/min-agent-loop && uv run python code.py
```

试试这些 prompt（教学 demo 会执行模型生成的 shell 命令，建议在临时目录里玩）：

1. `Create a file called hello.py that prints "Hello, World!"`
2. `List all Python files in this directory`
3. `What is the current git branch?`

观察重点：模型什么时候调用工具（循环继续）、什么时候不调用（循环结束）？

## 验收标准

1. 准备一个含简单 bug 的小脚本（如一个测试不过的函数）。
2. 把「修好让测试通过」作为任务交给你的 loop。
3. agent 能自主：读文件 → 定位 → 写修复 → 跑测试确认 → 结束。

## 参考（先读再写）

- learn-claude-code [s01_agent_loop](https://github.com/shareAI-lab/learn-claude-code/tree/main/s01_agent_loop)（含 CC 源码 `query.ts` 对照）。
- [DeepSeek Function Calling 文档](https://api-docs.deepseek.com/guides/function_calling)。
- [How to Build an Agent（Thorsten Ball）](https://ampcode.com/notes/how-to-build-an-agent)。

## 进阶（可选，对应 s02–s04）

- 给它更多结构化工具（read_file / write_file / list），看模型会不会一次调多个工具。
- 加最大轮数保护、危险命令权限确认（s03）、PreToolUse 钩子（s04）。
- 用 SWE-bench Lite 的一个实例当真实任务跑一遍。

> 写完可让 `harness-code-reviewer` 子智能体审阅：loop 终止条件、tool 消息回填、id 配对、轮数保护。
