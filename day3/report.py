"""Day 3 实战：读设备巡检 CSV → 清洗 → 生成 JSON 报告

运行：
    python report.py
    python day3/report.py      # 从仓库根也行

分工：
    csv_loader.py   读 CSV、数字转换、清洗
    report.py       统计、输出、自检
"""

import json
from pathlib import Path

from csv_loader import clean_rows, load_rows

BASE = Path(__file__).resolve().parent
CSV_PATH = BASE / "devices.csv"
JSON_PATH = BASE / "report.json"


def build_report(devices: list) -> dict:
    """【只写这里】统计三项，组成报告字典。

    输入的 devices 长这样（清洗后的干净数据）：
        [{"设备编号": "M-001", "名称": "1号冷却泵", "类型": "泵",
          "功率": 7.5, "电流": 14.2, "温度": 58.0, "状态": "运行"}, ...]

    要返回的字典（键名要一模一样）：
        {
            "设备总数": 9,
            "状态统计": {"运行": 7, "检修": 1, "报警": 1},
            "功率总计": 77.7,
        }

    ★ 第一项最简单：len(devices)

    ★ 第二项（状态统计）用"计数惯用法"：
        counts = {}
        for d in devices:
            state = d["状态"]
            counts[state] = counts.get(state, 0) + 1

    ★ 第三项（功率总计）注意功率可能是 None：
        total = 0.0
        for d in devices:
            if d["功率"] is not None:
                total += d["功率"]
      最后 round(total, 2) 保留两位小数
    """
    report = {}

    # ---- 1. 设备总数 ----
    # TODO
    report["设备总数"] = len(devices)
    # ---- 2. 状态统计 ----
    # TODO
    counts = {}
    for d in devices:
        state = d["状态"]
        counts[state] = counts.get(state, 0) + 1
    report["状态统计"] = counts
    # ---- 3. 功率总计 ----
    # TODO
    total = 0.0
    for d in devices:
        if d["功率"] is not None:      # 功率可能是 None，跳过
            total += d["功率"]
    report["功率总计"] = round(total, 2)
    return report


def save_json(path: str, data: dict) -> None:
    """把报告写成 JSON 文件（已写好，不用改）。"""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def print_report(report: dict) -> None:
    """打印报告（已写好，不用改）。"""
    print("=" * 40)
    print("设备巡检报告")
    print("=" * 40)
    print(f"设备总数：{report.get('设备总数', '?')} 台")
    print(f"功率总计：{report.get('功率总计', '?')} kW")
    print("状态分布：")
    for state, count in (report.get("状态统计") or {}).items():
        print(f"    {state}：{count} 台")
    print("【本报告由程序自动生成】")
    print("=" * 40)


# ============================================================ 自动检查（不要改）


def _check(report: dict) -> None:
    ok = 0
    total = 3

    if report.get("设备总数") == 9:
        ok += 1
        print("  OK 设备总数 = 9")
    else:
        print(f"  X  设备总数：期望 9，你给了 {report.get('设备总数')!r}")

    want_state = {"运行": 7, "检修": 1, "报警": 1}
    if report.get("状态统计") == want_state:
        ok += 1
        print(f"  OK 状态统计 = {want_state}")
    else:
        print(f"  X  状态统计：期望 {want_state}，你给了 {report.get('状态统计')!r}")

    power = report.get("功率总计")
    if isinstance(power, (int, float)) and abs(float(power) - 77.7) < 0.01:
        ok += 1
        print(f"  OK 功率总计 = {power}")
    else:
        print(f"  X  功率总计：期望 77.7，你给了 {power!r}")

    print()
    print("=" * 56)
    print(f"核对 {ok} / {total}")
    if ok == total:
        print("三项全对，今天的任务完成了。")
        print("想多练再做明天剩下的（类型统计、温度统计），不想做就收工。")
    print("=" * 56)


if __name__ == "__main__":
    rows = load_rows(CSV_PATH)
    print(f"读到 {len(rows)} 行原始数据")

    devices = clean_rows(rows)
    print(f"清洗后 {len(devices)} 台设备\n")

    report = build_report(devices)
    print_report(report)
    save_json(JSON_PATH, report)

    print()
    _check(report)
