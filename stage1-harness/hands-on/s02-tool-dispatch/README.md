# 动手锚点 · s02 工具分发（Tool Dispatch）

> 对照 learn-claude-code [s02_tool_use](https://github.com/shareAI-lab/learn-claude-code/tree/main/s02_tool_use)。
> **一句话**：s01 的 `while` 循环一行不改——把硬编码的 `run_bash(...)` 换成查表
> `TOOL_HANDLERS[name](**args)`，工具从 1 个扩到 5 个。加一个工具 = TOOLS 加一条 schema + 字典加一行。

## 这一课新增了什么

| 组件 | s01 | s02 |
|---|---|---|
| 工具数量 | 1（bash） | 5（+ read_file / write_file / edit_file / glob） |
| 工具执行 | 硬编码 `run_bash(...)` | `TOOL_HANDLERS` 查表分发 |
| 路径安全 | 无 | `safe_path` 校验（仅 file 工具） |
| 循环 | `while True` + tool_calls | **完全一致，未改** |

## 准备

```sh
cd stage1-harness/hands-on/s02-tool-dispatch
cp ../min-agent-loop/.env .env      # 复用 s01 已填好的 key（.env 已被 .gitignore 忽略）
```

依赖无新增（`openai` + `python-dotenv`，已在仓库根装好）。

## 你要写的（3 处 TODO，脚手架里已标注）

1. **四个工具实现** `run_read / run_write / run_edit / run_glob`
   —— 用已给好的 `safe_path()` 守护路径，出错就 `return "Error: ..."`。每个函数 docstring 里有提示。
2. **`TOOL_HANDLERS` 分发字典** —— 工具名 → 处理函数，注册全部 5 个。
   key 必须与 `TOOLS` 里的 `name` 完全一致（`read_file` → `run_read`）。
3. **`agent_loop` 里查表分发那几行** —— s02 唯一的循环改动：
   ```python
   handler = TOOL_HANDLERS.get(call.function.name)
   out = handler(**args) if handler else f"Unknown tool: {call.function.name}"
   messages.append({"role": "tool", "tool_call_id": call.id, "content": out})
   ```

> 周边（run_bash / safe_path / 5 个 TOOLS schema / CLI / loop 外壳）已给好。

## 运行 & 验收

```sh
uv run python code.py
```

试这些 prompt，观察「何时调一个工具、何时一次调多个」：

1. `Read README.md and tell me what this project is about`（单工具：read_file）
2. `Create test.py that prints "hello", then read it back`（多步：write_file → read_file）
3. `Find all Python files here`（glob）
4. `Read both README.md and code.py, then write a summary to notes.txt`（一次可能返回多个 tool_calls）

**验收标准**：5 个工具都能被正确分发执行；多工具调用按顺序处理、各回一条 tool 消息；
模型基于真实工具结果作答（而非编造）。

## 进阶（可选，对应 README「深入 CC 源码」）

- **并发**：教学版按 `tool_calls` 顺序逐个执行。CC 用 `isConcurrencySafe` 把只读工具分批并发、写工具串行。
  可以试着把只读工具（read/glob/`bash ls`）并发跑。
- **结果落盘**：给工具结果加 `maxResultSizeChars`，超限落盘只回预览 + 路径（s02 附录提到的 FileRead 无限循环坑）。

> 写完可让 `harness-code-reviewer` 子智能体审阅：分发 key 对齐、`**args` 展开、safe_path 是否真挡住 `../` 逃逸。
