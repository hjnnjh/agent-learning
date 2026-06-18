#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""s02 工具层测试 —— 测 TODO 1（4 个工具）+ TODO 2（TOOL_HANDLERS 分发）。

不依赖 API、不跑循环（TODO 3 用交互式验证）。
import 前先 chdir 到临时目录并设占位 key，使 code.py 的 WORKDIR 锚定到 tmp、
OpenAI client 能构造（不连网），所有文件读写都隔离在临时目录里。

Run:
    uv run pytest test_tools.py -v
"""

import importlib.util
import os
import tempfile
from pathlib import Path

import pytest

# ── 隔离环境：tmp 工作区 + 占位 key，必须在 import code.py 之前 ──
_TMP = Path(tempfile.mkdtemp(prefix="s02_test_")).resolve()
os.chdir(_TMP)
os.environ.setdefault("DEEPSEEK_API_KEY", "sk-test-dummy")

# 用 importlib 按路径加载，避免与标准库的 `code` 模块同名冲突
_spec = importlib.util.spec_from_file_location("s02code", Path(__file__).parent / "code.py")
s02 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(s02)


def test_write_then_read():
    assert "Wrote" in s02.run_write("a.txt", "hello\nworld")
    assert s02.run_read("a.txt") == "hello\nworld"


def test_read_limit():
    s02.run_write("b.txt", "l1\nl2\nl3")
    assert s02.run_read("b.txt", limit=2) == "l1\nl2"


def test_edit_replaces_once():
    s02.run_write("c.txt", "foo bar foo")
    s02.run_edit("c.txt", "foo", "X")
    assert s02.run_read("c.txt") == "X bar foo"  # 只替换第一处


def test_edit_missing_text_returns_error():
    s02.run_write("d.txt", "abc")
    assert "Error" in s02.run_edit("d.txt", "zzz", "y")


def test_glob_finds_py_files():
    s02.run_write("g1.py", "")
    s02.run_write("g2.py", "")
    out = s02.run_glob("*.py")
    assert "g1.py" in out and "g2.py" in out


def test_safe_path_blocks_escape():
    with pytest.raises(ValueError):
        s02.safe_path("../escape.txt")


def test_handlers_match_tool_schema():
    """TOOL_HANDLERS 的 key 必须与 TOOLS 里声明的 name 完全对齐，且都可调用。"""
    schema_names = {t["function"]["name"] for t in s02.TOOLS}
    assert set(s02.TOOL_HANDLERS) == schema_names
    assert all(callable(fn) for fn in s02.TOOL_HANDLERS.values())


def test_dispatch_through_handlers():
    """模拟 loop 里的查表分发：handler(**args)。"""
    handler = s02.TOOL_HANDLERS.get("write_file")
    assert handler is not None
    out = handler(**{"path": "e.txt", "content": "x"})
    assert "Wrote" in out
