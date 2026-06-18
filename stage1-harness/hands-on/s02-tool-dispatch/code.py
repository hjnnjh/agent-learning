#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""s02 Tool Use — 工具分发（DeepSeek / OpenAI-compatible）。

s02 的唯一新概念：**工具分发（dispatch map）**。
循环一行不用改——只把 s01 里硬编码的 `run_bash(...)` 换成查表 `TOOL_HANDLERS[name](**args)`。
加一个工具 = TOOLS 数组加一条 schema + TOOL_HANDLERS 字典加一行映射。

本文件已给好：run_bash（s01 复用）、safe_path（路径安全）、5 个工具的 TOOLS schema、CLI、loop 外壳。
**留你手写（3 处 TODO）**：
  1. run_read / run_write / run_edit / run_glob 四个工具实现的函数体；
  2. TOOL_HANDLERS 分发字典（注册全部 5 个工具）；
  3. agent_loop 里「查表分发」那几行。

OpenAI 格式备忘（与 s01 一致）：
  - 工具名： call.function.name
  - 参数：  json.loads(call.function.arguments) → dict，可用 **args 展开传给 handler
  - 结果回灌：{"role": "tool", "tool_call_id": call.id, "content": out}

Run:
    cp ../min-agent-loop/.env .env   # 复用已填好的 key（.env 已被 .gitignore 忽略）
    uv run python code.py
"""

import json
import os
import subprocess
from pathlib import Path

try:
    import readline  # noqa: F401

    readline.parse_and_bind("set bind-tty-special-chars off")
    readline.parse_and_bind("set input-meta on")
    readline.parse_and_bind("set output-meta on")
    readline.parse_and_bind("set convert-meta off")
except ImportError:
    pass

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

WORKDIR = Path.cwd()
client = OpenAI(
    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
    api_key=os.environ["DEEPSEEK_API_KEY"],
)
MODEL = os.getenv("MODEL_ID", "deepseek-chat")
SYSTEM = f"You are a coding agent at {WORKDIR}. Use tools to solve tasks. Act, don't explain."


# ── FROM s01 (unchanged) ──
def run_bash(command: str) -> str:
    """Run a shell command, return combined stdout+stderr (truncated to 50k)."""
    dangerous = ["rm -rf /", "sudo", "shutdown", "reboot", "> /dev/"]
    if any(d in command for d in dangerous):
        return "Error: Dangerous command blocked"
    try:
        r = subprocess.run(
            command,
            shell=True,
            cwd=WORKDIR,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=120,
        )
        out = (r.stdout + r.stderr).strip()
        return out[:50000] if out else "(no output)"
    except subprocess.TimeoutExpired:
        return "Error: Timeout (120s)"
    except (FileNotFoundError, OSError) as e:
        return f"Error: {e}"


# ── 路径安全（给好）：把相对路径锚定到 WORKDIR，拒绝逃逸到工作区之外 ──
def safe_path(p: str) -> Path:
    """Resolve `p` under WORKDIR; raise if it escapes the workspace."""
    path = (WORKDIR / p).resolve()
    if not path.is_relative_to(WORKDIR):
        raise ValueError(f"Path escapes workspace: {p}")
    return path


# ── TODO 1：四个工具实现（用 safe_path 守护文件路径；出错就 return "Error: ..."）──
def run_read(path: str, limit: int | None = None) -> str:
    """Read a file's text. If `limit` set, return only the first `limit` lines.

    提示：safe_path(path).read_text().splitlines() → 取前 limit 行 → "\\n".join(...)
    """
    lines = safe_path(path).read_text().splitlines()
    if limit:
        lines = lines[:limit]
    return "\n".join(lines)


def run_write(path: str, content: str) -> str:
    """Write `content` to `path` (create parent dirs). Return a short confirmation.

    提示：fp = safe_path(path); fp.parent.mkdir(parents=True, exist_ok=True); fp.write_text(content)
    """
    safe_path(path).write_text(content)
    return f"Wrote {len(content)} bytes to {path}."


def run_edit(path: str, old_text: str, new_text: str) -> str:
    """Replace `old_text` with `new_text` once. Error if `old_text` not present.

    提示：读出 text；if old_text not in text → return error；text.replace(old_text, new_text, 1) 写回
    """
    text = safe_path(path).read_text()
    if old_text not in text:
        return "Error: text not found"
    safe_path(path).write_text(text.replace(old_text, new_text, 1))
    return f"Edited {path}"


def run_glob(pattern: str) -> str:
    """Return newline-joined paths matching `pattern` under WORKDIR.

    提示：import glob; glob.glob(pattern, root_dir=WORKDIR)；无匹配返回 "(no matches)"
    """
    import glob as g

    return "\n".join(g.glob(pattern, root_dir=WORKDIR))


# ── 工具定义（给好）：5 个工具的 OpenAI function-calling schema ──
def _fn(name: str, description: str, props: dict, required: list[str]) -> dict:
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": props,
                "required": required,
            },
        },
    }


TOOLS = [
    _fn(
        "bash",
        "Run a shell command.",
        {"command": {"type": "string"}},
        ["command"],
    ),
    _fn(
        "read_file",
        "Read file contents.",
        {"path": {"type": "string"}, "limit": {"type": "integer"}},
        ["path"],
    ),
    _fn(
        "write_file",
        "Write content to a file.",
        {"path": {"type": "string"}, "content": {"type": "string"}},
        ["path", "content"],
    ),
    _fn(
        "edit_file",
        "Replace exact text in a file once.",
        {
            "path": {"type": "string"},
            "old_text": {"type": "string"},
            "new_text": {"type": "string"},
        },
        ["path", "old_text", "new_text"],
    ),
    _fn(
        "glob",
        "Find files matching a glob pattern.",
        {"pattern": {"type": "string"}},
        ["pattern"],
    ),
]


# ── TODO 2：分发映射（工具名 → 处理函数）。注册全部 5 个工具。──
# 注意：字典 key 必须与上面 TOOLS 里的 name 完全一致（read_file → run_read，等）。
TOOL_HANDLERS = {
    # "bash": run_bash,
    # ... 你来补全
    "bash": run_bash,
    "read_file": run_read,
    "write_file": run_write,
    "edit_file": run_edit,
    "glob": run_glob,
}


# ── agent_loop — 与 s01 结构一致，只改「工具执行」那几行（查表分发）──
def agent_loop(messages: list) -> None:
    while True:
        resp = client.chat.completions.create(
            model=MODEL, messages=messages, tools=TOOLS
        )
        msg = resp.choices[0].message
        messages.append(msg)
        if resp.choices[0].finish_reason != "tool_calls":
            return
        for call in msg.tool_calls:
            args = json.loads(
                call.function.arguments
            )  # noqa: F841  # TODO 3 里 handler(**args) 会用到
            # ── TODO 3：查表分发（s02 的核心，只有这几行是新的）──
            #   1. handler = TOOL_HANDLERS.get(call.function.name)
            #   2. out = handler(**args) if handler else f"Unknown tool: {call.function.name}"
            #   3. 回灌一条 {"role": "tool", "tool_call_id": call.id, "content": out}
            #   （可在执行前 print(f"\033[33m> {call.function.name}\033[0m") 观察调了哪个工具）
            handler = TOOL_HANDLERS.get(call.function.name)
            out = (
                handler(**args)
                if handler
                else f"Unknown tool: {call.function.name}"
            )
            print(f"\033[33m> {call.function.name}\033[0m")
            messages.append(
                {"role": "tool", "tool_call_id": call.id, "content": out}
            )


if __name__ == "__main__":
    print("s02: Tool Use — 工具分发 (DeepSeek)")
    print("输入问题，回车发送。输入 q 退出。\n")

    history: list = [{"role": "system", "content": SYSTEM}]
    while True:
        try:
            query = input("\033[36ms02 >> \033[0m")
        except (EOFError, KeyboardInterrupt):
            break
        if query.strip().lower() in ("q", "exit", ""):
            break
        history.append({"role": "user", "content": query})
        agent_loop(history)
        final = history[-1]
        text = (
            final.get("content")
            if isinstance(final, dict)
            else getattr(final, "content", None)
        )
        if text:
            print(text)
        print()
