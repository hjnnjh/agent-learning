# 动手锚点 · 最小 Agent Loop

> **目标**：不用任何 agent 框架，直接用原生 LLM API 写一个 while 循环，给它 **bash** 和
> **文件读写** 两个工具，让它能修一个简单 bug。这是阶段一的硬指标——大量 harness 直觉只能从这里得到。

## 必须自己写（不要让 Claude 代劳）

循环骨架（伪代码）：

```
messages = [user_task]
while True:
    resp = call_model(messages, tools=[bash, read_file, write_file])
    if resp 没有 tool_use:           # 模型认为做完了
        print(resp.text); break
    for call in resp.tool_use:        # 执行每个工具调用
        result = run_tool(call)       # bash / 读 / 写
        messages.append(tool_result(call.id, result))
    messages.append(assistant(resp))  # 把模型这轮输出也放回上下文
```

## 验收标准

1. 准备一个含简单 bug 的小脚本（如一个测试不过的函数）。
2. 把「修好让测试通过」作为任务交给你的 loop。
3. agent 能自主：读文件 → 定位 → 写修复 → 跑测试确认 → 结束。

## 参考（先读再写）

- [How to Build an Agent（Thorsten Ball）](https://ampcode.com/notes/how-to-build-an-agent) — 一个下午照着写。
- [Tool use with Claude（文档）](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) — 消息协议。
- [claude-cookbooks: patterns/agents](https://github.com/anthropics/claude-cookbooks/tree/main/patterns/agents)
- learn-claude-code s01–s04（agent loop / 工具分发 / 权限 / hooks）。

## 进阶（可选）

- 加 `think` 工具、加最大轮数保护、加权限确认。
- 用 SWE-bench Lite 的一个实例当真实任务跑一遍。

> 依赖用 `uv add anthropic`（或 openai）。写完可让 `harness-code-reviewer` 子智能体审阅。
