"""Day 5 实验一：token 不等于字数，也不是免费的。

用法（在 ai-learning 目录下）：
    .venv\\Scripts\\python day5\\token_lab.py

它做两件事：
    1. 拿不同长度的中英文文本，只问"有多少 token"，算出「字符 / token」的比例
    2. 让模型真写一段 200 字，量一次输出的 token、耗时和花费

注意：这个脚本会真的调 API，总共花几分钱。
"""

import os
import time

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv("DEEPSEEK_API_KEY", "").strip()
BASE_URL = os.getenv("LLM_BASE_URL", "https://api.deepseek.com").strip()
MODEL = os.getenv("LLM_MODEL", "deepseek-chat").strip()

# 元 / 百万 token，跟 hello_llm.py 保持一致
PRICE_IN = 2.0
PRICE_OUT = 8.0

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

SEED_ZH = "电气自动化专业的核心课程包括电机拖动、PLC 编程、传感器与检测技术。"
SEED_EN = "Electrical engineering covers motors, PLC programming, sensors and measurement."


def count_tokens(text: str) -> int:
    """只问不答：让它回一个字符，读回包里的 prompt_tokens。

    max_tokens=1 是为了把输出成本压到最低——我们只关心输入有多少 token。
    """
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": text + "\n\n只回复 OK"}],
        temperature=0,
        max_tokens=1,
    )
    return resp.usage.prompt_tokens


def main() -> None:
    print(f"模型：{MODEL}\n")

    print(f"{'样本':<12}{'字符数':>8}{'token':>8}{'字符/token':>13}{'输入成本(元)':>14}")
    print("-" * 60)

    rows = []
    for times in (1, 5, 20, 80):
        text = SEED_ZH * times
        n = count_tokens(text)
        cost = n / 1_000_000 * PRICE_IN
        rows.append((len(text), n))
        print(f"{'中文 x' + str(times):<12}{len(text):>8}{n:>8}{len(text) / n:>13.2f}{cost:>14.6f}")

    for times in (1, 5, 20):
        text = SEED_EN * times
        n = count_tokens(text)
        cost = n / 1_000_000 * PRICE_IN
        rows.append((len(text), n))
        print(f"{'英文 x' + str(times):<12}{len(text):>8}{n:>8}{len(text) / n:>13.2f}{cost:>14.6f}")

    total_chars = sum(c for c, _ in rows)
    total_tokens = sum(t for _, t in rows)
    print("-" * 60)
    print(f"合计：{total_chars} 字符 → {total_tokens} token，平均 {total_chars / total_tokens:.2f} 字符/token")
    print(f"这些测量本身花了 {total_tokens / 1_000_000 * PRICE_IN:.6f} 元\n")

    print("=== 第二部分：一次真实输出值多少钱 ===")
    question = "用中文写一段 200 字左右的说明，介绍设备巡检为什么需要知识库。"
    start = time.time()
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": question}],
        temperature=0,
        max_tokens=400,
    )
    elapsed = time.time() - start

    n_in = resp.usage.prompt_tokens
    n_out = resp.usage.completion_tokens
    cost = n_in / 1_000_000 * PRICE_IN + n_out / 1_000_000 * PRICE_OUT
    text = resp.choices[0].message.content or ""

    print(f"输入 token：{n_in}（提问）")
    print(f"输出 token：{n_out}（回答 {len(text)} 字）")
    print(f"耗时      ：{elapsed:.2f} 秒")
    print(f"花费      ：{cost:.6f} 元")
    print(f"输出占比  ：{n_out / (n_in + n_out) * 100:.1f}% 的 token 是输出")
    print()
    print("记住这个结构：输入便宜、输出贵 4 倍，而且长上下文每次都要重发一遍。")


if __name__ == "__main__":
    main()
