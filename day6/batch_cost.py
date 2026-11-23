"""Day 6 任务 4：50 条批量抽取 + 成本统计。

用法（在 ai-learning 目录下）：
    .venv\\Scripts\\python day6\\batch_cost.py

它做的事：
    1. 用模板批量生成 50 条设备报警文本（不手打）
    2. 逐条让模型抽成结构化 JSON（设备 / 现象 / 类别）
    3. 校验字段，缺字段算失败
    4. 累计 token 与花费，打印汇总，写 batch_result.csv
"""

import csv
import time
from pathlib import Path

from day6 import llm
from day6.llm import LAST_USAGE, ask_json, cost_of

# ---------------------------------------------------------------- 造数据

DEVICES = [
    "1号冷却泵", "3号线ABB ACS880", "2号空压机", "5号皮带输送机", "1号除尘风机",
    "4号液压站", "2号搅拌电机", "6号包装机", "3号真空泵", "1号空压机",
]

PHENOMENA = [
    "{设备} 报 F0009，面板显示逆变单元过温，风扇声音异常",
    "{设备} 振动 8.2 mm/s，超过报警值 7.1 mm/s",
    "{设备} 轴承温度 92℃，比昨天高 15℃",
    "{设备} 出口压力掉到 0.15MPa，达不到工艺要求",
    "{设备} 运行电流波动大，空载电流偏高",
]

REQUIRED_KEYS = ("设备", "现象", "类别")
ALLOWED_CATEGORY = {"机械", "电气", "工艺", "其他"}

PROMPT_TMPL = """把下面的设备报警整理成 json，只返回一个 json 对象，不要解释。字段：
- 设备：字符串，设备名称
- 现象：字符串，原文里的报警内容，不要补充原文没有的原因
- 类别：只能取 机械 / 电气 / 工艺 / 其他 之一

报警：{text}"""


def make_samples(n: int = 50) -> list[str]:
    samples = []
    for device in DEVICES:
        for tmpl in PHENOMENA:
            samples.append(tmpl.format(设备=device))
            if len(samples) >= n:
                return samples
    return samples


# ---------------------------------------------------------------- 抽取


def extract_one(text: str) -> dict:
    """抽一条，并校验字段。不合法就抛 ValueError。"""
    data = ask_json(PROMPT_TMPL.format(text=text))

    missing = [k for k in REQUIRED_KEYS if k not in data]
    if missing:
        raise ValueError(f"缺字段：{missing}")

    category = data.get("类别")
    if category not in ALLOWED_CATEGORY:
        raise ValueError(f"类别不在允许范围：{category!r}")
    return data


# ---------------------------------------------------------------- 主流程


def main() -> None:
    samples = make_samples(50)
    print(f"生成 {len(samples)} 条报警文本\n")

    rows = []
    ok = fail = 0
    total_in = total_out = 0

    start = time.time()

    for idx, text in enumerate(samples, 1):
        try:
            data = extract_one(text)

            total_in += LAST_USAGE["prompt_tokens"]
            total_out += LAST_USAGE["completion_tokens"]
            ok += 1

            rows.append({
                "序号": idx,
                "原文": text,
                "设备": data.get("设备", ""),
                "现象": data.get("现象", ""),
                "类别": data.get("类别", ""),
                "状态": "ok",
                "错误": "",
            })
            print(f"[{idx:2d}/50] ok    {data.get('设备', '')} / {data.get('类别', '')}")

        except Exception as exc:
            fail += 1
            rows.append({
                "序号": idx,
                "原文": text,
                "设备": "", "现象": "", "类别": "",
                "状态": "fail",
                "错误": f"{type(exc).__name__}: {exc}",
            })
            print(f"[{idx:2d}/50] FAIL  {type(exc).__name__}: {exc}")

    elapsed = time.time() - start

    out = Path(__file__).resolve().parent / "batch_result.csv"
    with out.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else [])
        writer.writeheader()
        writer.writerows(rows)

    print("\n" + "=" * 50)
    print(f"完成 {len(samples)} 条：ok {ok} 条，失败 {fail} 条")
    print(f"总耗时 {elapsed:.1f} 秒，平均每条 {elapsed / len(samples):.2f} 秒")
    print(f"API 调用 {llm.CALL_COUNT} 次（应该等于 {len(samples)}，失败重试会更多）")
    print(f"输入 {total_in} token，输出 {total_out} token")
    print(f"总花费 {cost_of(total_in, total_out):.4f} 元")
    print(f"结果已写入 {out}")


if __name__ == "__main__":
    main()
