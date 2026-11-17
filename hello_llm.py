"""Day 1 任务：跑通第一个大模型 API 调用。

用法（在本目录下）：
    .venv\\Scripts\\python hello_llm.py

它会做三件事：
    1. 从 .env 里读 API Key（不写在代码里，避免泄露）
    2. 发一次请求给大模型，打印回答
    3. 打印 token 用量和估算花费

拿不到 Key 也没关系，脚本会告诉你缺什么。
"""

import os
import sys
import time

from dotenv import load_dotenv
from openai import OpenAI

# ---------------------------------------------------------------- 配置
# load_dotenv() 会读取同目录下的 .env 文件，把里面的变量塞进环境变量
load_dotenv()

API_KEY = os.getenv("DEEPSEEK_API_KEY", "").strip()
BASE_URL = os.getenv("LLM_BASE_URL", "https://api.deepseek.com").strip()
MODEL = os.getenv("LLM_MODEL", "deepseek-chat").strip()

# 价格常量（元 / 百万 token）。各家各时期不同，以官网价目表为准，变了改这里。
PRICE_INPUT = 2.0
PRICE_OUTPUT = 8.0

# --------------------------------------------------------- 今天要问的问题
# 想换问题，只改下面这一行「引号中间」的文字。
# 注意：引号必须成对，PROMPT = " 和结尾的 " 都不要动。
PROMPT = "给一家做工业视觉检测的创业公司起 5 个名字，每个配一句理由。"

# 想换回 Day 1 的原题，把上面那行前面加 # 注释掉，再把下面这行前面的 # 去掉：
# PROMPT = "用一句话解释什么是电气自动化，再举一个工厂里的真实例子。"

# ------------------------------------------------------------------------
# 温度：0 = 尽量稳定（同样的问题答案基本一样）；1 = 更随机（措辞会变）
TEMPERATURE = 0


def check_api_key() -> bool:
    """检查 Key 是否配置好，没配置就打印操作指引并返回 False。"""
    if not API_KEY or API_KEY.startswith("sk-xxx"):
        print("=" * 60)
        print("[!] 没找到 DEEPSEEK_API_KEY，或者还是示例里的占位符。")
        print()
        print("怎么办：")
        print("  1. 打开 https://platform.deepseek.com 注册并创建 API Key")
        print("  2. 在本目录下把 .env.example 复制成 .env")
        print("  3. 用记事本打开 .env，把 sk-xxx 换成你自己的 Key")
        print("  4. 保存后重新运行本脚本")
        print("=" * 60)
        return False
    return True


def main() -> int:
    if not check_api_key():
        return 1

    print(f"模型：{MODEL}")
    print(f"接口：{BASE_URL}")
    print(f"温度：{TEMPERATURE}")
    print(f"提问：{PROMPT}")
    print("-" * 60)

    # OpenAI 客户端兼容任何"OpenAI 兼容接口"，DeepSeek 就是其中之一
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    start = time.time()
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": PROMPT}],
            temperature=TEMPERATURE,
        )
    except Exception as exc:  # 网络、Key 错误、余额不足都会走到这里
        print(f"[x] 调用失败：{type(exc).__name__}: {exc}")
        print()
        print("常见原因：")
        print("  - Key 复制错了或缺字符")
        print("  - 账户没有余额")
        print("  - 网络不通（试试关闭代理，或反过来开启代理）")
        return 1
    elapsed = time.time() - start

    answer = resp.choices[0].message.content
    print(answer)
    print("-" * 60)

    usage = resp.usage
    n_in, n_out = usage.prompt_tokens, usage.completion_tokens
    cost = n_in / 1_000_000 * PRICE_INPUT + n_out / 1_000_000 * PRICE_OUTPUT

    print(f"耗时      : {elapsed:.2f} 秒")
    print(f"输入 token: {n_in}")
    print(f"输出 token: {n_out}")
    print(f"估算花费  : {cost:.6f} 元")
    print()
    print("[OK] 环境是通的。Day 1 的核心验收点完成了。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
