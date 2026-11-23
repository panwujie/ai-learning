"""Day 6：把"调大模型"封装成一个可复用的小模块。

以后每个脚本 import 它就行，不用再抄一遍 client 初始化、不用再记价格常量。

用法（在 ai-learning 目录下）：
    .venv\\Scripts\\python -c "from day6.llm import ask; print(ask('用一句话解释 PLC'))"

或者别的脚本里：
    from llm import ask, ask_json, ask_stream
"""

import json
import os
import time

from dotenv import load_dotenv
from openai import BadRequestError, OpenAI

load_dotenv()

MODEL = os.getenv("LLM_MODEL", "deepseek-chat").strip()
BASE_URL = os.getenv("LLM_BASE_URL", "https://api.deepseek.com").strip()

# 元 / 百万 token
PRICE_IN = 2.0
PRICE_OUT = 8.0

# 最近一次调用的用量，批量脚本靠它累计成本
LAST_USAGE = {"prompt_tokens": 0, "completion_tokens": 0}

# 真正发出去的 API 请求次数，用来抓“循环多跑了一遍”这类烧钱 bug
CALL_COUNT = 0

_client = None


def client() -> OpenAI:
    """懒加载：第一次调用时才读 Key、建客户端。

    好处：模块被 import 时不会因为没配 Key 就崩，只有真调用时才报错。
    """
    global _client
    if _client is None:
        key = os.getenv("DEEPSEEK_API_KEY", "").strip()
        if not key or key.startswith("sk-xxx"):
            raise RuntimeError("没找到 DEEPSEEK_API_KEY，检查 ai-learning/.env")
        _client = OpenAI(api_key=key, base_url=BASE_URL)
    return _client


def cost_of(prompt_tokens: int, completion_tokens: int) -> float:
    """按当前价格算一次调用的钱（元）。"""
    return prompt_tokens / 1_000_000 * PRICE_IN + completion_tokens / 1_000_000 * PRICE_OUT


def ask(prompt: str, system: str | None = None, temperature: float = 0, max_tokens: int = 800) -> str:
    """发一次普通对话，返回文本内容。"""
    global CALL_COUNT

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    resp = client().chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    CALL_COUNT += 1
    LAST_USAGE["prompt_tokens"] = resp.usage.prompt_tokens
    LAST_USAGE["completion_tokens"] = resp.usage.completion_tokens
    return (resp.choices[0].message.content or "").strip()


def ask_json(prompt: str, system: str | None = None, retries: int = 2) -> dict:
    """要求模型只返回 JSON，解析成 dict。解析失败就重试。
    
    提示（写的时候按这个来）：
      1. 调用时加 response_format={"type": "json_object"}
      2. 提示词里必须出现 "json" 这个词，否则接口会直接报错
      3. json.loads 可能失败（模型偶尔会多写解释、少括号），用 try/except 包住
      4. 失败时把上一次的错误也塞回提示词，让它自己修正，比原样重试有效
      5. 最后一次还失败，就抛异常，别静默返回 {}
    """
    global CALL_COUNT

    if "json" not in prompt.lower():
        prompt = prompt.rstrip() + "\n\n请只返回一个 JSON 对象，不要任何解释或代码块。"
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    last_error = ""
    for attempt in range(retries + 1):
        try:
            resp = client().chat.completions.create(
                model=MODEL,
                messages=messages,
                temperature=0,
                response_format={"type": "json_object"},
            )
        except BadRequestError:
            raise
        except Exception as exc:
            last_error = f"{type(exc).__name__}: {exc}"
            if attempt == retries:
                raise
            continue
        CALL_COUNT += 1
        LAST_USAGE["prompt_tokens"] = resp.usage.prompt_tokens
        LAST_USAGE["completion_tokens"] = resp.usage.completion_tokens
        raw  = (resp.choices[0].message.content or "").strip()   # 先拿到干净的字符串
        try:
            return json.loads(raw)                 # 成功就立刻 return，别继续循环
        except json.JSONDecodeError as exc:
            last_error = str(exc)
            messages.append({"role": "assistant", "content": raw})
            messages.append({
                "role": "user",
                "content": f"你刚才返回的不是合法 JSON：{exc}\n请只输出合法 JSON。",
            })
    raise ValueError(f"重试 {retries} 次后仍无法解析 JSON：{last_error}")                              

def ask_stream(prompt: str, system: str | None = None, temperature: float = 0) -> str:
    """流式输出：边生成边打印，最后返回完整文本。

    提示（写的时候按这个来）：
      1. create(..., stream=True) 返回的是一个迭代器，不是完整响应
      2. 每块在 chunk.choices[0].delta.content，可能是 None（最后一块）
      3. print(..., end="", flush=True) 才有"一点点冒出来"的效果
      4. 把每块拼起来，最后一起 return
      5. 流式模式下拿不到 usage，要么自己按字符估算，要么不统计
    """
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    resp = client().chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=temperature,
        stream=True,                 # ← 关键：返回迭代器，不是完整响应
    )
    start = time.time()
    首字 = None
    full = ""
    for chunk in resp:
        delta = chunk.choices[0].delta.content
        if delta:                    # 最后一块是 None，不判断会 TypeError
            if 首字 is None:
                首字 = time.time() - start
            full += delta
            print(delta, end="", flush=True)
    print()
    print(f"首字 {首字:.2f}s，总共 {time.time() - start:.2f}s")
    return full
    
