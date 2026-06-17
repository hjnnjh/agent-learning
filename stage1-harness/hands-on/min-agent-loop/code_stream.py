#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""s01 Agent Loop — 流式版骨架（DeepSeek / OpenAI-compatible）。

在非流式版（code.py）跑通后再做这一关。
流式唯一的新难点：stream=True 时 tool_calls 是「分片」到达的——
要按 tc.index 把碎片归并，并把 function.arguments 的字符串「逐段拼接」，
全部收完才能 json.loads。文本(content)与工具碎片在同一个流里交错到达。

骨架已给：开流 / 边到边打印 / 消息还原 / 工具执行 / 轮数上限 / 异常兜底。
**唯一留白：delta 累加（见 TODO）。** 没填之前，纯文本任务能跑（会流式打印），
但带工具的任务因为 tool_calls 累加为空，会被当成「做完了」而不执行工具——填好就通。

Run:
    uv run python code_stream.py
"""

import json
import os
import subprocess

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

client = OpenAI(
    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
    api_key=os.environ["DEEPSEEK_API_KEY"],
)
MODEL = os.getenv("MODEL_ID", "deepseek-chat")
SYSTEM = f"You are a coding agent at {os.getcwd()}. Use bash to solve tasks. Act, don't explain."

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


def stream_agent_loop(messages: list, max_turns: int = 20) -> None:
    """流式循环。每轮：开流 → 累加碎片 → 还原一条 assistant 消息 → 执行工具 → 续。"""
    for _ in range(max_turns):
        stream = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            stream=True,
        )

        content = ""  # 文本增量在这里累加
        tool_calls: dict[int, dict] = {}  # tc.index -> {"id", "name", "args"}

        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta.content:
                content += delta.content
                print(
                    f"\033[90m{delta.content}\033[0m", end="", flush=True
                )  # 边到边打印
            if delta.tool_calls:
                for tc in delta.tool_calls:
                    # ── TODO（流式核心，你来写）────────────────────────────────
                    # tc 是一个「碎片」，不是完整工具调用。按 tc.index 归并：
                    #   1. slot = tool_calls.setdefault(
                    #          tc.index, {"id": None, "name": None, "args": ""})
                    #   2. 第一片带 tc.id 与 tc.function.name（后续片为 None）→ 有就存进 slot。
                    #   3. 每片可能带一段 tc.function.arguments 字符串碎片 → 用 += 拼到 slot["args"]。
                    # 关键：arguments 是「字符串逐段拼接」，不是 dict.update，也不是覆盖。
                    slot = tool_calls.setdefault(
                        tc.index, {"id": None, "name": None, "args": ""}
                    )
                    if tc.id:
                        slot["id"] = tc.id
                    if tc.function and tc.function.name:
                        slot["name"] = tc.function.name
                    if tc.function and tc.function.arguments:
                        slot["args"] += tc.function.arguments
                    # ──────────────────────────────────────────────────────────
        print()

        # 把累加结果还原成一条 assistant 消息（OpenAI tool_calls 格式），append 回上下文
        if tool_calls:
            messages.append(
                {
                    "role": "assistant",
                    "content": content or None,
                    "tool_calls": [
                        {
                            "id": tool_calls[i]["id"],
                            "type": "function",
                            "function": {
                                "name": tool_calls[i]["name"],
                                "arguments": tool_calls[i]["args"],
                            },
                        }
                        for i in sorted(tool_calls)
                    ],
                }
            )
        else:
            # 没有工具调用 = 模型做完了。
            # 流式下别只信 finish_reason（可能来得晚/缺）；看「有没有 tool_calls」更稳。
            messages.append({"role": "assistant", "content": content})
            return

        # 执行每个工具调用，结果各回一条 tool 消息
        for i in sorted(tool_calls):
            slot = tool_calls[i]
            print(f"\033[33m$ {slot['args']}\033[0m")
            try:
                args = json.loads(slot["args"])
                out = run_bash(args["command"])
            except (json.JSONDecodeError, KeyError) as e:
                out = (
                    f"Error: bad tool arguments: {e}"  # 错误回灌，让模型自己改
                )
            print(out[:200])
            messages.append(
                {"role": "tool", "tool_call_id": slot["id"], "content": out}
            )

    print(f"\033[31m[stopped] 达到 max_turns={max_turns}\033[0m")


if __name__ == "__main__":
    print("s01: Agent Loop — 流式版 (DeepSeek)")
    print("输入问题，回车发送。输入 q 退出。\n")

    history: list = [{"role": "system", "content": SYSTEM}]
    while True:
        try:
            query = input("\033[36ms01-stream >> \033[0m")
        except (EOFError, KeyboardInterrupt):
            break
        if query.strip().lower() in ("q", "exit", ""):
            break
        history.append({"role": "user", "content": query})
        stream_agent_loop(history)
        print()
