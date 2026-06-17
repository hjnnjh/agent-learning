#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Smoke test: one DeepSeek chat round-trip (no tools, no loop).

Verifies that `.env` is wired and the API key works before you write the loop.
Run: `uv run python check_api.py`
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

client = OpenAI(
    base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
    api_key=os.environ["DEEPSEEK_API_KEY"],
)
model = os.getenv("MODEL_ID", "deepseek-chat")


def main() -> None:
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "ping — reply with the single word: pong"}],
    )
    print(f"model={model}  reply={resp.choices[0].message.content!r}")
    print(f"usage={resp.usage}")


if __name__ == "__main__":
    main()
