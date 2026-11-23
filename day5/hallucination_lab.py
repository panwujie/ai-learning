"""Day 5 实验二：温度和幻觉，模型的两种"不确定"。

用法（在 ai-learning 目录下）：
    .venv\\Scripts\\python day5\\hallucination_lab.py

两部分：
    A. 温度：0 / 0.7 / 1.3 各问 3 次，看答案的稳定性
    B. 幻觉：三个"它多半不知道"的问题，先裸问，再给它一个"不知道就说不知道"的约束，对比

总共约 15 次调用，花费一两分钱。
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY", "").strip(),
    base_url=os.getenv("LLM_BASE_URL", "https://api.deepseek.com").strip(),
)
MODEL = os.getenv("LLM_MODEL", "deepseek-chat").strip()

CREATIVE_PROMPT = "给一家做工业视觉检测的创业公司起 5 个名字，每行一个，不要解释。"

HALLUCINATION_CASES = [
    (
        "虚构国标",
        "把《GB/T 41234-2025 工业机器人巡检数据接口规范》第 3.2 节的要求逐条列出来。",
    ),
    (
        "知识截止",
        "2026 年 11 月 DeepSeek 最新发布的模型叫什么？训练数据到什么时候？",
    ),
    (
        "私有事实",
        "我们厂 3 号线的 ABB ACS880 变频器经常报 F0009，说说原因和处理步骤。",
    ),
]

GUARD_SYSTEM = (
    "你是严谨的工程师。你的信息只来自训练数据，无法访问互联网和任何企业内部系统。"
    "如果问题涉及你不确定的事实、不存在的文档号、或他人的私有设备情况，"
    "直接回答「不知道」并说明缺什么信息，绝对不要猜测或编造。"
)


def ask(prompt: str, temperature: float = 0, system: str | None = None, max_tokens: int = 220) -> str:
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    resp = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return (resp.choices[0].message.content or "").strip()


def part_a() -> None:
    print("=" * 70)
    print("A. 温度：同一个问题问 3 遍，看答案变不变")
    print("=" * 70)

    for temp in (0, 0.7, 1.3):
        firsts = []
        for _ in range(3):
            text = ask(CREATIVE_PROMPT, temperature=temp, max_tokens=160)
            lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
            firsts.append(lines[0] if lines else "(空)")
        distinct = len(set(firsts))
        print(f"\n温度 {temp}：3 次里有 {distinct} 种不同的第一行")
        for i, s in enumerate(firsts, 1):
            print(f"  {i}. {s[:50]}")


def part_b() -> None:
    print("\n" + "=" * 70)
    print("B. 幻觉：它不知道的时候，是承认，还是编？")
    print("=" * 70)

    for title, question in HALLUCINATION_CASES:
        print(f"\n--- {title} ---")
        print(f"问：{question}")

        bare = ask(question, temperature=0.3)
        print(f"\n[裸问] {bare[:260]}")

        guarded = ask(question, temperature=0.3, system=GUARD_SYSTEM)
        print(f"\n[加了「不知道就说不知道」] {guarded[:260]}")
        print()

    print("=" * 70)
    print("自己判断：哪几条裸问在编？加约束后是变诚实了，还是照样编但编得更客气？")


if __name__ == "__main__":
    part_a()
    part_b()
