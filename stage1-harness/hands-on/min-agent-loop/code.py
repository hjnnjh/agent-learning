#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""s01 Agent Loop — DeepSeek (OpenAI-compatible).

最小 agent harness 内核：一个 while 循环，模型调用工具就继续，不调用就停。
本文件已备好 client / 工具定义 / run_bash / CLI；**核心 agent_loop 留给你手写**。

Run:
    uv run python code.py
"""

import json  # noqa: F401  # 你写的 agent_loop 里会用到（json.loads 解析工具参数）
import os
import subprocess

try:
    import readline  # noqa: F401

    # macOS 的 libedit 在处理中文输入时有退格问题，这四行修复它
    readline.parse_and_bind("set bind-tty-special-chars off")
    readline.parse_and_bind("set input-meta on")
    readline.parse_and_bind("set output-meta on")
    readline.parse_and_bind("set convert-meta off")
except ImportError:
    pass

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

client = OpenAI(
    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
    api_key=os.environ["DEEPSEEK_API_KEY"],
)
MODEL = os.getenv("MODEL_ID", "deepseek-chat")

SYSTEM = f"You are a coding agent at {os.getcwd()}. Use bash to solve tasks. Act, don't explain."

# ── Tool definition: just bash (OpenAI function-calling format) ──
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "bash",
            "description": "Run a shell command.",
            "parameters": {
                "type": "object",
                "properties": {"command": {"type": "string"}},
                "required": ["command"],
            },
        },
    }
]


# ── Tool execution ──
def run_bash(command: str) -> str:
    """Execute a shell command, return combined stdout+stderr (truncated to 50k)."""
    dangerous = ["rm -rf /", "sudo", "shutdown", "reboot", "> /dev/"]
    if any(d in command for d in dangerous):
        return "Error: Dangerous command blocked"
    try:
        r = subprocess.run(
            command,
            shell=True,
            cwd=os.getcwd(),
            capture_output=True,
            text=True,
            timeout=120,
        )
        out = (r.stdout + r.stderr).strip()
        return out[:50000] if out else "(no output)"
    except subprocess.TimeoutExpired:
        return "Error: Timeout (120s)"
    except (FileNotFoundError, OSError) as e:
        return f"Error: {e}"


# ── 动手锚点：核心循环留给你手写 ──
def agent_loop(messages: list) -> None:
    """The agent loop — YOU write this (s01 的动手锚点)。

    把这 5 步翻译成代码（OpenAI / DeepSeek 语义）：

      1. 把 messages + TOOLS 发给模型：
           resp = client.chat.completions.create(
               model=MODEL, messages=messages, tools=TOOLS)
      2. 取本轮回复 msg = resp.choices[0].message，append 回 messages。
      3. 若 resp.choices[0].finish_reason != "tool_calls" → 模型做完了，return。
      4. 否则遍历 msg.tool_calls，对每个 call：
           args = json.loads(call.function.arguments)
           out  = run_bash(args["command"])
         把结果作为一条 {"role": "tool", "tool_call_id": call.id, "content": out}
         append 回 messages。
      5. 回到第 1 步（while True）。

    提示：
      - msg 是 OpenAI 对象，append 时直接放它即可（SDK 负责序列化）。
      - DeepSeek 一次可能返回多个 tool_calls：每个都要执行、各回一条 tool 消息。
      - 可在执行前 print 一下命令（如黄色 \\033[33m），方便观察循环。
    """
    while True:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS
        )
        msg = resp.choices[0].message
        messages.append(msg)
        if resp.choices[0].finish_reason != "tool_calls":
            return
        else:
            for call in msg.tool_calls:
                args = json.loads(call.function.arguments)
                out = run_bash(args["command"])
                messages.append(
                    {"role": "tool", "tool_call_id": call.id, "content": out}
                )


# ── Entry point ──
if __name__ == "__main__":
    print("s01: Agent Loop (DeepSeek)")
    print("输入问题，回车发送。输入 q 退出。\n")

    history: list = [{"role": "system", "content": SYSTEM}]
    while True:
        try:
            query = input("\033[36ms01 >> \033[0m")
        except (EOFError, KeyboardInterrupt):
            break
        if query.strip().lower() in ("q", "exit", ""):
            break
        history.append({"role": "user", "content": query})
        agent_loop(history)
        # Print the model's final text reply
        final = history[-1]
        text = (
            final.get("content")
            if isinstance(final, dict)
            else getattr(final, "content", None)
        )
        if text:
            print(text)
        print()
